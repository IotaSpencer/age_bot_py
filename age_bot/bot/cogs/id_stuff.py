# built-in

# 3rd party
import discord
from discord import ApplicationContext, Message, SlashCommandGroup
from discord.ext import commands
from discord.commands import \
    slash_command

# local
from age_bot.config import Config, ServerDB
from age_bot.bot.helpers.decorators import Decorators
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

        if ctx.channel



    # @commands.command()
    # @has_attachment()
    # async def verify(self, ctx: commands.Context, *, guild: discord.Guild = None):
    #     if guild:
    #         member = await guild.fetch_member(ctx.author.id)
    #         file_url = ctx.message.attachments.first.url
    #         db_guild = ServerDB.servers.to_dict()[str(guild.id)]
    #         verify_channel = db_guild.verify_channel
    #         channel = await guild.fetch_channel(verify_channel)
    #         confirm_msg = await channel.send("""
    #             {file_url}
    #                   To add the 'Adult' role to this user, enter the following:
    #                   `{prefix}confirm $XXXXX$ "#{user_distinct}"`
    
    #                   Sent as of #{timestamp} UTC
    
    #                   To reject this user use the message ID and a reasonable reason--
    
    #                   `{prefix}reject $XXXXX$ "#{user_distinct}" "username is photoshopped in"`
    #                   or 
    #                   `{prefix}reject $XXXXX$ "#{user_distinct}" "user is not 18+"`
    #                   or
    #                   `{prefix}reject $XXXXX$ "#{user_distinct}" "XXXXX is needed as well as XXXXX in the same shot"`
    #                   or 
    #                   `{prefix}reject $XXXXX$ "#{user_distinct}" "XXXXX is needed see #id-example"`
    
    #                   The given reason will be sent to the user. So be nice and concise.
    #             """.format(timestamp=ctx.message.created_at, file_url=file_url,
    #                        user_distinct=member_distinct(ctx, member), prefix=ctx.bot.command_prefix))
    #         msg_id = confirm_msg.id
    #         edited_msg = confirm_msg.content.replace('$XXXXX$', msg_id)
    #         await confirm_msg.edit(content=edited_msg)
    #         await member.send("Your submission has been sent.")
    #         logger.debug('Making sure we sent our message')
    #         await member.send("If you haven't received a message that your submission has been sent, let the admins of "
    #                           "the applicable server know to contact the owner of this bot(iotaspencer#0001).")

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
