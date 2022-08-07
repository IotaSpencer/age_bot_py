# built-in
import asyncio
import re
# 3rd party
from typing import Union

from discord.ext import commands
from discord import Cog, Member
from discord.ext.commands import Context
from discord import Message, slash_command, ApplicationContext
import discord
# local
from age_bot.bot.helpers import calculate_age
from age_bot.bot.helpers.discord_helpers import get_adult_role, check_if_tester_or_main_bot, member_distinct, \
    has_server_confirm_role, reply_self_is_dev
from age_bot.loggers import logger
from age_bot.config import Configs
from age_bot.bot.helpers.perms_predicate import confirmable_check
from age_bot.exceptions import ConfirmPermError


class Confirm(Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.confirm'

    @slash_command(name="adultify",
                   description="Manually add the 'adult' role to a member if they can't use the verification system",
                   usage="<user> <dob: DD/MM/YYYY format>",
                   default_permission=False)
    async def slash_adultify(self, ctx: ApplicationContext, user: discord.Member = None, dob: str = None):
        """[user] [dob]"""
        if check_if_tester_or_main_bot(ctx, self.bot):
            disclaimer_reply = None
            await ctx.defer(ephemeral=True)
            author = ctx.user
            age = calculate_age(dob)
            adult_role = await get_adult_role(ctx)
            guild = ctx.guild_id
            db_guild = Configs.sdb.servers[str(guild)]
            guild = ctx.guild
            verify_channel = db_guild.verify_channel
            channel = await guild.fetch_channel(verify_channel)
            if has_server_confirm_role(guild, ctx.author):
                try:

                    await ctx.respond(
                        "Are you sure you want to add the 'adult' role to {}? (yes/no)".format(user.mention),
                        ephemeral=True)
                    await ctx.respond(f"This user is according to you, {age}", ephemeral=True)
                    await ctx.respond(
                        "Please make sure to check that the ID+Tag photo is a valid submission and that the user is 18+",
                        ephemeral=True)

                    def check(m: Message) -> bool:
                        return re.search(r"""^(Y(es)?|[Nn](o)?)""", m.content, re.IGNORECASE) is not None and \
                               m.author.id == ctx.author.id and m.author.id == ctx.user.id

                    msg = await ctx.bot.wait_for('message', timeout=30.0, check=check)
                    match msg.content:
                        case 'Yes' | 'yes' | 'Y' | 'y' | 'YES':
                            disclaimer_reply = True
                        case 'No' | 'no' | 'N' | 'n' | 'NO':
                            disclaimer_reply = False
                    if isinstance(disclaimer_reply, bool):
                        await user.add_roles(adult_role)
                        await ctx.respond(
                            "{} has been given the 'adult' role".format(user.mention),
                            ephemeral=True)
                        audit_log_string = f"{ctx.user.mention} manually gave {user.mention} the {adult_role} Role."
                        await user.add_roles(adult_role, reason=audit_log_string)
                        e = discord.Embed(title="Manual Adult")
                        e.set_author(name=ctx.author)
                        e.add_field(name="Action", value=audit_log_string)
                        e.add_field(name="Input", value=f"{dob}")
                        e.colour = adult_role.color
                        await ctx.respond(content="Command Triggered.", ephemeral=True)
                        await channel.send(embed=e)  # sends the embed
                        await user.send(content=f"You've been confirmed to be a(n) {adult_role.name} on {ctx.guild.name}")
                except asyncio.TimeoutError:
                    await ctx.respond(content=f"Sorry, you have 30 seconds to decide. Try again or forget it.")

            else:
                await ctx.respond(content="You don't have permission to change user roles.")
                e = discord.Embed(title="Failed Adult")
                e.set_author(name=ctx.author)
                e.add_field(name='No Permission', value="User does not have permission to change user roles")
                await ctx.respond("You don't have permission to change user roles")
                await channel.send(embed=e)
        else:
            await reply_self_is_dev(ctx)

    @commands.command(usage="<message> <user>", description="Confirm an ID as valid")
    @confirmable_check()
    async def confirm(self, ctx: Context, message: int, user: str):
        member = ctx.guild.get_member_named(user)
        adult_role = await get_adult_role(ctx)
        msg = await ctx.channel.fetch_message(message)
        try:

            if not member.get_role(adult_role.id):
                await member.add_roles(adult_role, reason='Moderator adulted member')
                await ctx.channel.send(
                    f"{member} was confirmed to be an {adult_role}".format(member=member_distinct(member),
                                                                           adult_role=adult_role.name))
                await member.send("You've been confirmed for '{adult_role}'".format(adult_role=adult_role.name))
            else:
                await ctx.channel.send(
                    "{member} already has the role {adult_role}.".format(member=member_distinct(member),
                                                                         adult_role=adult_role.name))
        finally:
            await msg.delete()

    @confirm.error
    async def confirm_error(self, ctx, error: Union[
            commands.MissingAnyRole, commands.MemberNotFound, commands.MessageNotFound, ConfirmPermError]):
        # if isinstance(error, TypeError):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send(
                "You are not allowed to use this command, you're missing all of these roles ({error})".format(
                    error=error.missing_roles))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(
                "This user is not in this guild, or is not cached."
            )
        elif isinstance(error, commands.MessageNotFound):
            await ctx.reply(
                "This message does not exist, or is too old to delete through me, if need be, delete the message "
                "manually. "
            )
        elif isinstance(error, ConfirmPermError):
            await ctx.reply(f"""You do not have permission to use this command.""")
        elif isinstance(error, discord.HTTPException):
            assert isinstance(error, discord.HTTPException), "This is not a discord.HTTPException"
            if error.code == 50007:
                await ctx.send(
                    "Cannot send messages to this user, they have DMs disabled."
                )
            else:
                await ctx.send(
                    "An HTTP Exception occurred while sending running the command. Please try again later or see the logs."
                )
                logger.error(f"A discord error occurred via the REST/HTTP API.\n"
                             f"Error Code: {error.code}\n"
                             f"Error Args: {error.args}\n"
                             f"Error Status: {error.status}\n"
                             f"Error Response: {error.response.text}")
        else:
            import traceback
            await ctx.reply(''.join(traceback.format_exception(
                type(error), error, error.__traceback__)))

    # noinspection PyTypeChecker
    @confirmable_check()
    @commands.command(usage="<message> <user> <reason...>", description="Reject an ID.")
    async def reject(self, ctx: Context, message: int, user: str, reason: str):
        member = ctx.guild.get_member_named(user)  # type: Member
        msg = ''
        try:
            msg = await ctx.channel.fetch_message(message)  # type: Message
        finally:
            await ctx.channel.send(f"{user} was rejected on grounds of \"{reason}\"")
            await msg.delete()
            await member.send(f"Your submission was rejected due to the reason — {reason}")
            await member.send(f"If applicable, try again later following the instructions laid out in the rejection "
                              f"message above.")

    @reject.error
    async def reject_error(self, ctx, error: Union[
            commands.MissingAnyRole, commands.MemberNotFound, commands.MessageNotFound, ConfirmPermError, discord.HTTPException]):
        if isinstance(error, commands.MissingAnyRole):
            assert isinstance(error, commands.MissingAnyRole)
            await ctx.send(
                f"You are not allowed to use this command, you're missing all of these roles ({error})".format(
                    error=error.missing_roles))
        elif isinstance(error, commands.MessageNotFound):
            assert isinstance(error, commands.MessageNotFound)
            await ctx.send(
                f"This message ({error.argument}) does not exist or is too old to delete. If need be, delete the message manually."
            )
        elif isinstance(error, commands.MemberNotFound):
            assert isinstance(error, commands.MemberNotFound)
            await ctx.send(
                f"This member ({error.argument}) does not exist, or is not in the cache"
            )
        elif isinstance(error, ConfirmPermError):
            await ctx.reply(f"""You do not have permission to use this command.""")
        elif isinstance(error, AttributeError):
            await ctx.reply(f"""This user left.""")
        elif isinstance(error, discord.HTTPException):
            assert isinstance(error, discord.HTTPException), "This is not a discord.HTTPException"
            if error.code == 50007:
                await ctx.send(
                    "Cannot send messages to this user, they have DMs disabled."
                )
            else:
                await ctx.send(
                    "An HTTP Exception occurred while sending running the command. Please try again later or see the logs."
                )
                logger.error(f"A discord error occurred via the REST/HTTP API.\n"
                             f"Error Code: {error.code}\n"
                             f"Error Args: {error.args}\n"
                             f"Error Status: {error.status}\n"
                             f"Error Response: {error.response.text}")
            await ctx.reply(f"{error}")
        else:
            import traceback
            await ctx.reply(''.join(traceback.format_exception(
                type(error), error, error.__traceback__)))


def setup(bot):
    bot.add_cog(Confirm(bot))
    logger.info('Loaded Confirm')


def teardown(bot):
    bot.remove_cog(Confirm(bot))
    logger.info('Unloaded Confirm')
