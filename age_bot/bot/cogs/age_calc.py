# built-in

import asyncio
from typing import Union

# 3rd party

from discord import ApplicationContext, Message, Member, User
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext

from discord.ext.commands import Context, Converter, Cog
import arrow as arw


# local imports
from age_bot.bot.helpers import calculate_age
from age_bot.config import Configs
from age_bot.loggers import logger


class AgeCalc(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.age_calc'

    @bridge.bridge_command(name='agecalc', description='calculates age of users')
    async def agecalc(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], dob: str):
        age = calculate_age(dob)
        await ctx.defer(ephemeral=True)
        await ctx.respond(age, ephemeral=True)


def setup(bot):
    bot.add_cog(AgeCalc(bot))
    logger.info('Loaded AgeCalc')


def teardown(bot):
    bot.remove_cog(AgeCalc(bot))
    logger.info('Unloaded AgeCalc')
