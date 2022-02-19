# built-in

# 3rd party
import asyncio

import discord
from discord.ext import commands
from discord import \
    ApplicationContext, SlashCommandGroup, Member, User, Message, \
    slash_command
from discord.commands import permissions

# local
from age_bot.logger import logger
from age_bot.config import Configs
from age_bot.bot.helpers.discord import *


class Confirm(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.confirm'

    @slash_command(name="adultify", description="Manually add the 'adult' role to a member",
                   guild_ids=[626522675224772658], default_permission=False)
    @permissions.has_any_role('Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner')
    async def slash_adultify(self, ctx: ApplicationContext, user: discord.Member = None):
        await ctx.defer()
        adult_role = ctx.guild.get_role(Configs.serverdb.servers[str(ctx.guild.id)].role)
        guild = ctx.guild_id
        db_guild = Configs.serverdb.servers[str(guild)]
        guild = ctx.guild
        verify_channel = db_guild.verify_channel
        channel = await guild.fetch_channel(verify_channel)
        audit_log_string = f"{ctx.user.mention} manually gave {user.mention} the {adult_role} Role."
        await user.add_roles(adult_role, reason=audit_log_string)
        e = discord.Embed()
        e.title("Manual Adult")
        e.set_author(name=ctx.author)
        e.add_field(name="Action", value=audit_log_string)
        e.colour = adult_role.color
        await ctx.respond()
        await channel.send(embed=e)  # sends the embed
        await user.send(content=f"You've been confirmed to be a(n) {adult_role.name} on {ctx.guild.name}")

    @commands.command(usage="<message> <user>", description="Confirm an ID as valid")
    @permissions.has_any_role('Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner')
    async def confirm(self, ctx: Context, message: int, user: str):
        global msg
        member = ctx.guild.get_member_named(user)
        adult_role = ctx.guild.get_role(Configs.serverdb.servers[str(ctx.guild.id)].role)
        msg = None
        try:

            if not member.get_role(adult_role.id):
                await member.add_roles(adult_role, reason='Moderator adulted member')
                msg = await ctx.channel.fetch_message(message)
                await ctx.channel.send(
                    f"{member} was confirmed to be an {adult_role}".format(member=member_distinct(ctx, member),
                                                                           adult_role=adult_role.name))
                await member.send("You've been confirmed for '{adult_role}'".format(adult_role=adult_role.name))
            else:
                msg = await ctx.channel.fetch_message(message)  # type: Message
                await ctx.channel.send(
                    "{member} already has the role {adult_role}.".format(member=member_distinct(ctx, member),
                                                                         adult_role=adult_role.name))
        finally:
            await msg.delete()

    @confirm.error
    async def confirm_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send(
                "You are not allowed to use this command, you're missing all of these roles ({error})".format(
                    error=error.missing_roles))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(
                "This user is not in this guild, or is not cached."
            )
        elif isinstance(error, commands.MessageNotFound):
            await ctx.send(
                "This message does not exist, or is too old to delete through me, if need be, delete the message manually."
            )

    @commands.command(usage="<message> <user> <reason...>", description="Reject an ID.")
    @permissions.has_any_role('Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner')
    async def reject(self, ctx: Context, message: int, user: str, reason: str):
        global msg
        member = ctx.guild.get_member_named(user)  # type: Member
        try:
            msg = await ctx.channel.fetch_message(message)  # type: Message
        finally:
            await ctx.channel.send(f"{user} was rejected on grounds of \"{reason}\"")
            await msg.delete()
            await member.send(f"Your submission was rejected due to the reason — {reason}")
            await member.send(f"If applicable, try again later following the instructions laid out in the rejection "
                          f"message above.")

    @reject.error
    async def reject_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send(
                f"You are not allowed to use this command, you're missing all of these roles ({error})".format(
                    error=error.missing_roles))
        if isinstance(error, commands.MessageNotFound):
            await ctx.send(
                f"This message ({error.argument}) does not exist or is too old to delete. If need be, delete the message manually."
            )
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(
                f"This member ({error.argument}) does not exist, or is not in the cache"
            )


def setup(bot):
    bot.add_cog(Confirm(bot))
    logger.info('Loaded Confirm')


def teardown(bot):
    bot.remove_cog(Confirm(bot))
    logger.info('Unloaded Confirm')
