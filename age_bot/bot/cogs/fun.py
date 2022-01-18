import discord
import logging
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply("Pong %sms" % ctx.bot.latency)




def setup(bot):
    bot.add_cog(Fun(bot))
    logging.info('Loaded Fun')

def teardown(bot):
    bot.remove_cog(Fun(bot))
    logging.info('Unloaded Fun')