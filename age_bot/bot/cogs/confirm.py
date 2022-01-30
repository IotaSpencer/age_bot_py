# built-in

# 3rd party
from discord import Message
from discord.ext import commands

# local
from age_bot.logger import logger
from age_bot.config import Config, ServerDB
from age_bot.bot.helpers.discord import *


class Confirm(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.confirm'

    @commands.command()
    @commands.has_any_role('Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner')
    async def confirm(self, ctx, message_id, user):
        member = ctx.guild.get_member_named(user)
        adult_role = ctx.guild.get_role(ServerDB.servers.to_dict()[str(ctx.guild.id)]['role'])
        if not member.get_role(adult_role.id):
            await member.add_roles(adult_role, reason='Moderator adulted member', atomic=True)
            msg = await ctx.channel.fetch_message(message_id)
            await ctx.channel.send(
                f"{member} was confirmed to be an {adult_role}".format(member=member_distinct(ctx, member),
                                                                       adult_role=adult_role.name))
            await member.send("You've been confirmed for '{adult_role}'".format(adult_role=adult_role.name))
            await msg.delete()

        else:
            msg: Message = await ctx.channel.fetch_message(message_id)
            await ctx.channel.send(
                "{member} already has the role {adult_role}.".format(member=member_distinct(ctx, member),
                                                                     adult_role=adult_role.name))
            await msg.delete()

    @confirm.error
    async def confirm_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send(
                "You are not allowed to use this command, you're missing all of these roles ({error})".format(
                    error=error.missing_roles))


def setup(bot):
    bot.add_cog(Confirm(bot))
    logger.info('Loaded Confirm')


def teardown(bot):
    bot.remove_cog(Confirm(bot))
    logger.info('Unloaded Confirm')
