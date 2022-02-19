# built-in

# 3rd party
import asyncio
from ctypes import Union
import discord
from discord import ApplicationContext, Message, SlashCommandGroup, Member, User
from discord.ext import commands
from discord.commands import \
    slash_command

# local
from age_bot.config import Configs
from age_bot.bot.helpers.decorators import is_other_bot_offline, is_valid_server_in_db
from age_bot.bot.helpers.discord import member_distinct
from age_bot.bot.helpers.exceptions import NoAttachmentError, TooManyAttachmentError
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

    @slash_command(name="verify", description="Verify your age via Nenrei-Sama", guild_ids=[626522675224772658])
    async def slash_verify(self, ctx: ApplicationContext):
        await ctx.defer()
        if ctx.channel.name == 'hello':
            member = ctx.author  # type: Union[Member, User]
            guild = ctx.guild_id
            db_guild = Configs.serverdb.servers[str(guild)]
            guild = ctx.guild
            verify_channel = db_guild.verify_channel
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
                              user_distinct=member_distinct(ctx, member),
                              prefix=ctx.bot.command_prefix))
                msg_id = confirm_msg.id
                edited_msg = confirm_msg.content.replace('$XXXXX$', str(msg_id))
                await confirm_msg.edit(content=edited_msg)
                await member.send("Your submission has been sent.")

            finally:
                logger.debug('Making sure we sent our message')
                await member.send(
                    "If you haven't received a message that your submission has been sent, let the admins of "
                    "the applicable server know to contact the owner of this bot(iotaspencer#0001).")

    # @commands.command()
    # @has_attachment()
    # async def verify(self, ctx: commands.Context, *, guild: discord.Guild = None):
    #     if guild:
    #         member = await guild.fetch_member(ctx.author.id)
    #         file_url = ctx.message.attachments.first.url
    #         db_guild = Configs.serverdb.servers.to_dict()[str(guild.id)]
    #         verify_channel = db_guild.verify_channel
    #         channel = await guild.fetch_channel(verify_channel)

    # @verify.error
    # async def verify_error(self, ctx, error):
    #     if isinstance(error, NoAttachmentError):
    #         await ctx.send("You are supposed to attach a file, the ID+Discord™ tag")
    #     if isinstance(error, TooManyAttachmentError):
    #         await ctx.send("""Hi, you're trying to send more than one photograph to me at a time.
    #                     Please only send one shot to me,
    #                     using the examples in the channel possibly called '#id-example'""")
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('Server ID is needed for verification')
    #         mutual_guilds = ctx.author.mutual_guilds
    #         guild_string = []
    #         for guild in mutual_guilds:
    #             guild_string.append("{0}({1})".format(guild.name, guild.id))
    #         await ctx.send("Applicable Server IDs are {0}".format(', '.join(guild_string)))
    #         await ctx.send(
    #             "Send your ID+tag (using the examples in #id-example and #upload-example), with one of the server IDs "
    #             "listed, the server ID is the number in parentheses.")
    #         await ctx.send("An example would be '{}verify 00000000000000000'".format(ctx.bot.command_prefix))


def setup(bot: discord.Bot):
    bot.add_cog(IDStuff(bot))
    logger.info('Loaded IDStuff')


def teardown(bot):
    bot.remove_cog(IDStuff(bot))
    logger.info('Unloaded IDStuff')
