# built-in

# 3rd Party
import discord
from discord.ext import commands

# local imports
from age_bot.bot.helpers.discord import member_distinct
from ...config import Configs
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
        await ctx.reply(f"""
            Hello, {member_distinct(ctx, ctx.author)}, in order to post or read {ctx.guild.name} messages you must be a certain role as well as 
            submitted a form of ID with the server in question.

            For {ctx.guild.name} that role is \
            {ctx.guild.get_role(Configs.serverdb.servers.to_dict()[str(ctx.guild.id)]['role'])} 

            To do so, please run the command /verify
            """)
        # .format(user=ctx.author.name, server_id=ctx.guild.id,
        # author_distinct=dhelpers.author_distinct(ctx), server_name=ctx.guild.name,
        # adult_role=ctx.guild.get_role(
        #    )

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
                            await shame_channel.send(
                                "{shamed_user} mentioned '#hello' in #hello at {shamed_time}".format(
                                    shamed_user=member_distinct(msg, shamed_user), shamed_time=shamed_time))
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
