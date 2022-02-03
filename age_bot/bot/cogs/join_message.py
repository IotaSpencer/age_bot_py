# built-in

# 3rd party
import discord
from discord.ext import commands

# local
from age_bot.logger import logger


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.join_message'

    @commands.Cog.listener()
    async def on_memping(self, ctx):
        await ctx.reply("Pong %sms" % ctx.bot.latency)




def setup(bot):
    bot.add_cog(Fun(bot))
    logger.info('Loaded Fun')

def teardown(bot):
    bot.remove_cog(Fun(bot))
    logger.info('Unloaded Fun')
