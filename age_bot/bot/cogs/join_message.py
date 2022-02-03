# built-in
import asyncio

# 3rd party
import discord
from discord.ext import commands
from discord import Member

# local
from age_bot.logger import logger


class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.join_message'

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        asyncio.sleep(60)



def setup(bot):
    bot.add_cog(JoinMessage(bot))
    logger.info('Loaded JoinM')

def teardown(bot):
    bot.remove_cog(Fun(bot))
    logger.info('Unloaded Fun')
