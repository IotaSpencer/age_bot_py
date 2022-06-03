# built-in

# 3rd party
import asyncio
from ctypes import Union
import discord
from discord import Member, User, Forbidden, TextChannel
from discord.ext import commands, bridge

# local
from discord.ext.commands import guild_only

from age_bot.config import Configs
from age_bot.bot.helpers.discord import *
from age_bot.exceptions import *
from age_bot.logger import logger


def has_attachment():
    def predicate(ctx):
        if len(ctx.message.attachments) == 1:
            return True
        elif len(ctx.message.attachments) > 1:
            raise TooManyAttachmentError
        else:
            raise NoAttachmentError

    return commands.check(predicate)


class IDStuff(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.id_stuff'

    @guild_only()
    @bridge.bridge_command(name="verify", description="Verify your age via Nenrei-Sama")
    async def verify(self, ctx):
        member = ctx.author  # type: Union[Member, User]
        guild = ctx.guild_id
        db_guild = Configs.serverdb.servers[str(guild)]
        guild = ctx.guild
        verify_channel = db_guild.verify_channel
        await ctx.defer(ephemeral=True)
        if ctx.channel.name == 'hello':
            try:
                await ctx.author.send("I'm going to wait for you to send a photo with an attachment,"
                                      " it can be an empty message. But there has to be a file attached.")
                await ctx.send_followup("Check your DMs", ephemeral=True)

                def check(m):
                    return len(m.attachments) == 1 and m.author.id == ctx.author.id

                try:
                    id_pic = await ctx.bot.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.author.send("Timeout while waiting for attachment.")
                    await ctx.author.send("Please try again later.")
                else:
                    channel = await guild.fetch_channel(verify_channel)
                    timestamp = id_pic.created_at
                    file_url = id_pic.attachments[0].url
                    confirm_msg = await channel.send(
                        ("{file_url}\n"
                         "To add the 'Adult' role to this user, enter the following:\n"
                         "`{prefix}confirm $XXXXX$ \"{user_distinct}\"`\n"
                         "\n"
                         "Sent as of {timestamp} UTC\n"
                         "\n"
                         "To reject this user use the message ID and a reasonable reason--\n"
                         "\n"
                         "`{prefix}reject $XXXXX$ \"{user_distinct}\" \"username is "
                         "photoshopped in\"`\n "
                         "or \n"
                         "`{prefix}reject $XXXXX$ \"{user_distinct}\" \"user is not 18+\"`\n"
                         "or\n"
                         "`{prefix}reject $XXXXX$ \"{user_distinct}\" \"XXXXX is needed as "
                         "well as XXXXX in the same shot\"`\n "
                         "or \n"
                         "`{prefix}reject $XXXXX$ \"{user_distinct}\" \"XXXXX is needed see "
                         "#id-example\"`\n "
                         "\n"
                         "The given reason will be sent to the user. So be nice and concise.\n"
                         ).format(timestamp=timestamp, file_url=file_url,
                                  user_distinct=member_distinct(member),
                                  prefix=ctx.bot.command_prefix))
                    msg_id = confirm_msg.id
                    edited_msg = confirm_msg.content.replace('$XXXXX$', str(msg_id))
                    await confirm_msg.edit(content=edited_msg)
                    await member.send("Your submission has been sent.")


            except Forbidden:
                hello_channel = Configs.serverdb.servers[str(ctx.guild.id)].hello_channel
                hello_chan = await ctx.guild.fetch_channel(hello_channel)  # type: TextChannel
                await hello_chan.send(
                    f"Hey {ctx.user.mention}, I can't seem to send you a message, please make sure you "
                    f"have accept messages from server members ticked. If you are really sure this is "
                    f"not the case. Then please say so in {hello_chan.mention}.", delete_after=120)


            finally:
                logger.debug('Making sure we sent our message')
                await member.send(
                    "If you haven't received a message that your submission has been sent, let the admins of "
                    "the applicable server know to contact the owner of this bot(iotaspencer#0001).")

    async def on_application_command_error(self, ctx, error):
        if isinstance(error, NoAttachmentError):
            await ctx.respond("You are supposed to attach a file, the ID+Discord™ tag")
        if isinstance(error, TooManyAttachmentError):
            await ctx.respond("""Hi, you're trying to send more than one photograph to me at a time.
                        Please only send one shot to me,
                        using the examples in the channel possibly called '#id-example'""")

        if isinstance(error, Forbidden):
            hello_channel = Configs.serverdb.servers[str(ctx.guild.id)].hello_channel
            hello_chan = await ctx.guild.fetch_channel(hello_channel)  # type: TextChannel
            await hello_chan.send(f"Hey {ctx.member.mention}, I can't seem to send you a message, please make sure you "
                                  f"have accept messages from server members ticked. If you are really sure this is "
                                  f"not the case. Then please say so in {hello_chan.mention}.", delete_after=120)

    async def on_command_error(self, ctx, error):
        if isinstance(error, NoAttachmentError):
            await ctx.respond("You are supposed to attach a file, the ID+Discord™ tag")
        if isinstance(error, TooManyAttachmentError):
            await ctx.respond("""Hi, you're trying to send more than one photograph to me at a time.
                        Please only send one shot to me,
                        using the examples in the channel possibly called '#id-example'""")

        if isinstance(error, Forbidden):
            hello_channel = Configs.serverdb.servers[str(ctx.guild.id)].hello_channel
            hello_chan = await ctx.guild.fetch_channel(hello_channel)  # type: TextChannel
            await hello_chan.send(f"Hey {ctx.member.mention}, I can't seem to send you a message, please make sure you "
                                  f"have accept messages from server members ticked. If you are really sure this is "
                                  f"not the case. Then please say so in {hello_chan.mention}.", delete_after=120)


def setup(bot: discord.Bot):
    bot.add_cog(IDStuff(bot))
    logger.info('Loaded IDStuff')


def teardown(bot):
    bot.remove_cog(IDStuff(bot))
    logger.info('Unloaded IDStuff')
