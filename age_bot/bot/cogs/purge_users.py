# built-in
from datetime import timedelta
from pathlib import Path
import asyncio

# 3rd party

import arrow
from discord import ApplicationContext, File
from discord import commands as acommands
from discord.ext import commands, bridge
from omegaconf.errors import ConfigKeyError
import yaml as YAML

# local imports
from age_bot.loggers import logger
from age_bot.exceptions import *
from age_bot.bot.helpers.discord_helpers import *
from chunk_list import chunks
from age_bot.bot.helpers.perms_predicate import *

async def run_purge(guild: Guild = None, users: list = None):
    if users is None:
        raise NoUsersToPurgeError
    if guild is None:
        raise NoGuildArgError
    chunked_users = chunks(users, 20)
    for part in chunked_users:
        for member in part:
            oldmem = member_distinct(guild.get_member(member))
            logger.info(f'Purging {oldmem}')
            await guild.kick(guild.get_member(member), reason="Purging inactive users.")
            logger.info(f"Purged inactive user {oldmem}")
        await asyncio.sleep(10)


class PurgeUsers(discord.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.purge_users'

    confirm_roles = ['Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner']

    @bridge.bridge_command(guild_id=626522675224772658)
    @acommands.guild_only()
    @confirmable_check()
    async def purge(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], wet: bool = False,
                    guild: Guild = None):
        """
            Purge server users
            :arg ctx: Context
            :arg wet: Whether to actually purge users, Defaults to wet == False
            :arg guild: Guild to use on (ID or <empty>) Empty uses the current guild if the context allows
        """
        await ctx.defer()
        guild = grab_guild(ctx)
        user = ctx.user
        if has_server_confirm_role(guild, user):
            if ctx.bot.is_ready():
                members = ctx.guild.fetch_members(limit=None)

                def predicate(m):
                    return not m.bot

                yml_object = {'users': {}}
                mem_list = await members.filter(predicate).flatten()
                not_adult = []
                for member in mem_list:
                    if is_not_adult(member, guild):
                        not_adult.append(member)
                today = arrow.now('US/Pacific')  # Discord's TimeZone
                grace_period = timedelta(seconds=1209600)

                for member in not_adult:
                    member_joined_date = member.joined_at
                    elapsed = today - member_joined_date
                    if elapsed > grace_period:
                        yml_object['users'][member_distinct(member)] = {
                            'id': member.id,
                            'elapsed': str(elapsed),
                            'roles': [role.name for role in member.roles if role.name != "@everyone"]
                        }
                if wet:
                    users = [dic['id'] for user, dic in yml_object['users'].items()]
                    await ctx.respond(content="Starting Purge.")
                    await run_purge(guild, users)
                    await ctx.respond(content="Finished Purge.")
                else:
                    with open(f"{Path.home()}/purge_log.yml", 'w') as file:

                        YAML.safe_dump(yml_object, file)
                    await ctx.respond('The Purge is near!', file=File(f"{Path.home()}/purge_log.yml"))
            else:
                await ctx.respond("Bot is not ready.")
        else:
            await ctx.respond(f"You do not have permission to use this command.")

    # @commands.Cog.listener()
    # async def on_application_command_error(self, ctx, error):
    #    if isinstance(error, GuildNotInDBError):
    #        await ctx.respond('Guild in question is not in serverdb.yml', ephemeral=True)

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #    if isinstance(error, GuildNotInDBError):
    #        await ctx.reply('Guild in question is not in serverdb.yml', delete_after=60)


def setup(bot):
    bot.add_cog(PurgeUsers(bot))
    logger.info('Loaded PurgeUsers')


def teardown(bot):
    bot.remove_cog(PurgeUsers(bot))
    logger.info('Unloaded PurgeUsers')
