# built-in
import asyncio
import re
# 3rd party

from discord.ext import commands
from discord.ext.commands import Converter
from discord import \
    Message, \
    slash_command

# local
from age_bot.logger import logger
from age_bot.bot.helpers.perms_predicate import *

class AgeConverter(Converter):
    async def convert(self, ctx, argument: str):
        now = arw.now()
        d_o_b = arw.get(argument, "DD/MM/YYYY")
        age = ((now.date().year - d_o_b.date().year) * 372 + (now.date().month - d_o_b.date().month) * 31 + (
                now.date().day - d_o_b.date().day)) / 372
        return str(age)

class Confirm(commands.Cog, command_attrs=dict(hidden=True)):
    confirm_roles = ['Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner']

    def __init__(self, bot):
        self.bot = bot
        self.confirm_roles = ['Discord moderator', 'Mods', 'Server manager', 'Sub overlord', 'Discord owner']

        self.ext_path = 'age_bot.bot.cogs.confirm'

    @commands.group('rej')
    async def rej(self, ctx):
        pass
    @rej.command()
    async def not_id_or_tag(self, ctx: Context, message: int, user: str, extra: str):
        member = ctx.guild.get_member_named(user)  # type: Member
        msg = {}
        try:
            msg = await ctx.channel.fetch_message(message)  # type: Message
        finally:
            apos = "'" if member.name[-1] == 's' else "'s"
            await ctx.channel.send(f"""{user}{apos} rejected, not an ID or discord tag with \"{extra}\" extra context.""")
            await msg.delete()
            await member.send(f"Your submission was rejected due to there not being an ID or discordtag in the photo")
            if extra:
                await member.send(f"Your rejection was given the following extra context — {extra}")
            await member.send(f"If applicable, try again later following the instructions laid out in the rejection "
                              f"message above.")

    @not_id_or_tag.error
    async def not_id_or_tag_error(self, ctx, error):
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

    @slash_command(name="adultify", description="Manually add the 'adult' role to a member",
                   default_permission=False)
    async def slash_adultify(self, ctx: ApplicationContext, user: discord.Member = None, dob: AgeConverter = None):
        await ctx.defer()
        author = ctx.user
        author_roles = author.roles
        author_named_roles = [role.name for role in author_roles]
        adult_role = await get_adult_role(ctx)
        guild = ctx.guild_id
        db_guild = Configs.serverdb.servers[str(guild)]
        guild = ctx.guild
        verify_channel = db_guild.verify_channel
        channel = await guild.fetch_channel(verify_channel)
        if has_server_confirm_role(guild, ctx.author):
            try:
                ctx.respond()
                def check(m: Message):
                    return re.search(r"""^([Yy](es)?|[Nn](o)?)""", m.content) is not None and m.author.id == ctx.author.id

                await ctx.bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.respond(content="Sorry, you have 1 minute to decide. Try again or forget it.")
            audit_log_string = f"{ctx.user.mention} manually gave {user.mention} the {adult_role} Role."
            await user.add_roles(adult_role, reason=audit_log_string)
            e = discord.Embed(title="Manual Adult")
            e.set_author(name=ctx.author)
            e.add_field(name="Action", value=audit_log_string)
            e.colour = adult_role.color
            await ctx.respond(content="Command Triggered.", ephemeral=True)
            await channel.send(embed=e)  # sends the embed
            await user.send(content=f"You've been confirmed to be a(n) {adult_role.name} on {ctx.guild.name}")
        else:
            await ctx.respond(content="You don't have permission to change user roles.")
            e = discord.Embed(title="Failed Adult")
            e.set_author(name=ctx.author)
            e.add_field(name='No Permission', value="User does not have permission to change user roles")
            await ctx.respond("You don't have permission to change user roles")
            await channel.send(embed=e)

    @commands.command(usage="<message> <user>", description="Confirm an ID as valid")
    @commands.check(predicate=confirmable_check)
    async def confirm(self, ctx: Context, message: int, user: str):
        member = ctx.guild.get_member_named(user)
        adult_role = await get_adult_role(ctx)
        msg = {}
        try:

            if not member.get_role(adult_role.id):
                await member.add_roles(adult_role, reason='Moderator adulted member')
                msg = await ctx.channel.fetch_message(message)
                await ctx.channel.send(
                    f"{member} was confirmed to be an {adult_role}".format(member=member_distinct(member),
                                                                           adult_role=adult_role.name))
                await member.send("You've been confirmed for '{adult_role}'".format(adult_role=adult_role.name))
            else:
                msg = await ctx.channel.fetch_message(message)  # type: Message
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
        if isinstance(error, commands.MemberNotFound):
            await ctx.reply(
                "This user is not in this guild, or is not cached."
            )
        if isinstance(error, commands.MessageNotFound):
            await ctx.reply(
                "This message does not exist, or is too old to delete through me, if need be, delete the message "
                "manually. "
            )
        if isinstance(error, ConfirmPermError):
            await ctx.reply(f"""You do not have permission to use this command.""")

    @commands.check(predicate=confirmable_check)
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
        if isinstance(error, commands.MessageNotFound):
            await ctx.send(
                f"This message ({error.argument}) does not exist or is too old to delete. If need be, delete the message manually."
            )
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(
                f"This member ({error.argument}) does not exist, or is not in the cache"
            )
        if isinstance(error, ConfirmPermError):
            await ctx.reply(f"""You do not have permission to use this command.""")


def setup(bot):
    bot.add_cog(Confirm(bot))
    logger.info('Loaded Confirm')


def teardown(bot):
    bot.remove_cog(Confirm(bot))
    logger.info('Unloaded Confirm')
