# built-in
from datetime import timedelta
from pathlib import Path

# 3rd party
from typing import Union

import arrow
from discord import ApplicationContext, Member, Guild, File
from discord.commands import permissions
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
from omegaconf.errors import ConfigKeyError
import yaml as YAML

# local imports
from age_bot.config import Configs
from age_bot.logger import logger
from age_bot.exceptions import GuildNotInDBError, NoGuildInContextError
from age_bot.bot.helpers.discord import member_distinct


class PurgeUsers(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.purge_users'

    confirm_roles = ['Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner']

    def grab_guild(self, ctx: ApplicationContext):
        if ctx.guild:
            return ctx.guild
        else:
            raise NoGuildInContextError

    def is_not_adult(self, member: Member, guild: Guild):
        """
        :rtype: bool
        :arg member: Guild Member
        :arg guild: Guild
        """
        try:
            adult_role = guild.get_role(Configs.serverdb.servers[str(guild.id)].role)
            member_roles = member.roles
            member_is_not_adult = adult_role not in member_roles
            return member_is_not_adult
        except ConfigKeyError:
            raise GuildNotInDBError

    @bridge.bridge_command(guild_ids=[626522675224772658], name='purge')
    @permissions.has_any_role('Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner',
                              'Server Helpers')
    async def purge(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], wet: bool = False,
                    guild: Guild = None):
        """
            Purge server users
            :arg ctx: Context
            :arg wet: Whether to actually purge users, Defaults to wet == False
            :arg guild: Guild to use on (ID or <empty>) Empty uses the current guild if the context allows
        """
        guild = guild or self.grab_guild(ctx)
        if ctx.bot.is_ready():
            members = ctx.guild.members
            for member in members:
                if self.is_not_adult(member, guild):
                    logger.info(f"{member} has '{member.roles}' roles")
            not_adult = [member for member in members if self.is_not_adult(member, guild)]

            today = arrow.now('US/Pacific')  # Discord's TimeZone
            grace_period = timedelta(seconds=1209600)
            yml_object = {'users': {}}
            for member in not_adult:
                member_joined_date = member.joined_at
                elapsed = today - member_joined_date
                if elapsed > grace_period:
                    yml_object['users'][member_distinct(member)] = {
                        'id': member.id,
                        'elapsed': str(elapsed)
                    }
            if wet:
                await ctx.respond("Not Implemented yet")
            else:
                with open(f"{Path.home()}/purge_log.yml", 'w') as file:
                    YAML.safe_dump(yml_object, file)
                await ctx.respond('The Purge is near!', file=File(f"{Path.home()}/purge_log.yml"))
        else:
            await ctx.respond("Bot is not ready.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, GuildNotInDBError):
            await ctx.respond('Guild in question is not in serverdb.yml')


def setup(bot):
    bot.add_cog(PurgeUsers(bot))
    logger.info('Loaded PurgeUsers')


def teardown(bot):
    bot.remove_cog(PurgeUsers(bot))
    logger.info('Unloaded PurgeUsers')
