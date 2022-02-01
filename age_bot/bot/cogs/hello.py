# built-in

# 3rd Party
import discord
from discord.ext import commands

# local imports
import age_bot.bot.helpers.discord as dhelpers
from ...config import Config, ServerDB
from age_bot.logger import logger


async def find_shamed(channels):
    for channel in channels:
        if channel.name == 'named-and-shamed':
            return channel
    return None


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.hello'

    @commands.command()
    async def hello(self, ctx):
        await ctx.reply("""
            Hello, {user}, in order to post or read {server_name} messages you must be a certain role as well as submitted a form of ID with the server in question.

            For {server_name} that role is {adult_role}

            To do so, please send me a picture of your ID with everything but your 'date of birth' blacked out along with some sort of Discord™ proof (Your account page with the email blacked out or a handwritten Discord™ tag)

            For you that would be {author_distinct}
            When you do so, attach this string below to the picture as a caption.

            &verify {server_id}""".format(user=ctx.author.name, server_id=ctx.guild.id,
                                          author_distinct=dhelpers.author_distinct(ctx), server_name=ctx.guild.name,
                                          adult_role=ctx.guild.get_role(
                                              ServerDB.servers.to_dict()[str(ctx.guild.id)]['role'])))

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        orig_msg = msg
        if msg.guild and msg.channel:
            if msg.channel.name == 'hello':
                if msg.channel_mentions:
                    if msg.channel_mentions[0].name == 'hello':
                        shame_msg = await msg.reply(content="The command is '&hello' nothing else"
                                                            "As per our above rules, as you mentioned the channel, "
                                                            "you shall be named and shamed.")
                        if await find_shamed(msg.guild.text_channels):
                            shame_channel = await find_shamed(msg.guild.text_channels)
                            shamed_user = msg.author
                            shamed_time = msg.created_at
                            await shame_channel.send("{shamed_user} mentioned '#hello' in #hello at {shamed_time}".format(
                                shamed_user=dhelpers.member_distinct(msg, shamed_user), shamed_time=shamed_time))
                            await shame_msg.delete(delay=10)
                            await msg.delete(delay=10)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            if msg.content.startswith('&') or msg.content.startswith('^'):
                await msg.author.send("Hello, I am a bot. If you have questions for me, ask someone in the server I "
                                      "share with you.")


def setup(bot):
    bot.add_cog(Hello(bot))
    logger.info('Loaded Hello')


def teardown(bot):
    bot.remove_cog(Hello(bot))
    logger.info('Unloaded Hello')
