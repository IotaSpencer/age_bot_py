# built-in
import asyncio
import re
# 3rd party

import arrow as arw
from discord.ext import commands
from discord import Cog
from discord.ext.commands import Converter, group, Context
from discord import Message, slash_command, ApplicationContext
import discord
# local
from age_bot.bot.helpers import calculate_age
from age_bot.bot.helpers.discord import get_adult_role, check_if_tester_or_main_bot, member_distinct
from age_bot.logger import logger
from age_bot.config import Configs
from age_bot.bot.helpers.perms_predicate import confirmable_check, helper_check
from age_bot.exceptions import ConfirmPermError, HelperPermError


class Confirm(Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.confirm'


    @slash_command(name="adultify", description="Manually add the 'adult' role to a member",
                   default_permission=False)
    async def slash_adultify(self, ctx: ApplicationContext, user: discord.Member = None, dob: str = None):
        """[user] [dob]"""
        if check_if_tester_or_main_bot(ctx, self.bot):
            await ctx.defer()
            author = ctx.user
            age = calculate_age(dob)
            author_roles = author.roles
            author_named_roles = [role.name for role in author_roles]
            adult_role = await get_adult_role(ctx)
            guild = ctx.guild_id
            db_guild = Configs.sdb.servers[str(guild)]
            guild = ctx.guild
            verify_channel = db_guild.verify_channel
            channel = await guild.fetch_channel(verify_channel)
            if has_server_confirm_role(guild, ctx.author):
                try:

                    await ctx.respond()

                    def check(m: Message) -> bool:
                        return re.search(r"""^(Y(es)?|[Nn](o)?)""", m.content) is not None and \
                               m.author.id == ctx.author.id and m.author.id == ctx.user.id

                    await ctx.bot.wait_for('message', timeout=60.0, check=check)
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
                    await ctx.respond(content="Sorry, you have 1 minute to decide. Try again or forget it.")

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
    async def confirm_error(self, ctx, error):
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
        else:
            import traceback
            await ctx.reply(''.join(traceback.format_exception(
                type(error), error, error.__traceback__)))

    @confirmable_check()
    @commands.command(usage="<message> <user> <reason...>", description="Reject an ID.")
    async def reject(self, ctx: Context, message: int, user: str, reason: str):
        member = ctx.guild.get_member_named(user)  # type: Member
        msg = {}
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
        elif isinstance(error, commands.MessageNotFound):
            await ctx.send(
                f"This message ({error.argument}) does not exist or is too old to delete. If need be, delete the message manually."
            )
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(
                f"This member ({error.argument}) does not exist, or is not in the cache"
            )
        elif isinstance(error, ConfirmPermError):
            await ctx.reply(f"""You do not have permission to use this command.""")
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

    # @group('rej')
    # async def rej(self, ctx):
    #     pass
    #
    # @rej.command()
    # async def not_id_or_tag(self, ctx: Context, message: int, user: str, extra: str):
    #     member = ctx.guild.get_member_named(user)  # type: Member
    #     msg = {}
    #     try:
    #         msg = await ctx.channel.fetch_message(message)  # type: Message
    #     finally:
    #         apos = "'" if member.name.endswith('s') else "'s"
    #         await ctx.channel.send(
    #             f"""{user}{apos} verification rejected, not an ID or discord tag with \"{extra}\" extra context.""")
    #         await msg.delete()
    #         await member.send(f"Your submission was rejected due to there not being an ID+discordtag in the photo")
    #         if extra:
    #             await member.send(f"Your rejection was given the following extra context — \"{extra}\"")
    #         await member.send(f"If applicable, try again later following the instructions laid out in the rejection "
    #                           f"message above.")
    #
    # @not_id_or_tag.error
    # async def not_id_or_tag_error(self, ctx, error):
    #     if isinstance(error, commands.MissingAnyRole):
    #         await ctx.send(
    #             f"You are not allowed to use this command, you're missing all of these roles ({error})".format(
    #                 error=error.missing_roles))
    #     if isinstance(error, commands.MessageNotFound):
    #         await ctx.send(
    #             f"This message ({error.argument}) does not exist or is too old to delete. If need be, delete the message manually."
    #         )
    #     if isinstance(error, commands.MemberNotFound):
    #         await ctx.send(
    #             f"This member ({error.argument}) does not exist, or is not in the cache"
    #         )