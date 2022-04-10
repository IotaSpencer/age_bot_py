# built-in

import asyncio
from ctypes import Union

# 3rd party

from discord import ApplicationContext, Message, Member, User
from discord.ext import commands, bridge
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext

from discord.ext.commands import Context, Converter, Cog
import arrow as arw


# local imports
from age_bot.config import Configs
from age_bot.logger import logger


class AgeConverter(Converter):
    async def convert(self, ctx, argument: str):
        now = arw.now()
        d_o_b = arw.get(argument, "DD/MM/YYYY")
        age = ((now.date().year - d_o_b.date().year) * 372 + (now.date().month - d_o_b.date().month) * 31 + (
                now.date().day - d_o_b.date().day)) / 372
        return str(age)


class AgeCalc(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.age_calc'

    @bridge.bridge_command(name='agecalc', description='calculates age of users')
    async def agecalc(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], age: AgeConverter):
        await ctx.defer(ephemeral=True)
        await ctx.respond(age, ephemeral=True)


def setup(bot):
    bot.add_cog(AgeCalc(bot))
    logger.info('Loaded AgeCalc')


def teardown(bot):
    bot.remove_cog(AgeCalc(bot))
    logger.info('Unloaded AgeCalc')
