# built-in

# 3rd party
import asyncio

from ctypes import Union

import discord
from discord import ApplicationContext, Message, Member, User
from discord.ext import commands
from discord.ext.commands import Context
from discord.commands import slash_command

import arrow as arw
# local imports
from age_bot.config import Configs
from age_bot.logger import logger


class AgeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        now = arw.now()
        d_o_b = arw.get(argument, "DD/MM/YYYY")
        age = ((now.date().year - d_o_b.date().year) * 372 + (now.date().month - d_o_b.date().month) * 31 + (
                now.date().day - d_o_b.date().day)) / 372
        return str(age)


class AgeCalc(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.age_calc'

    @commands.command(name='agecalc', aliases=['age'])
    async def agecalc(self, ctx: Context, age: AgeConverter):
        await ctx.reply(age, delete_after=60)

    @slash_command(name='agecalc', description='calculates age of users', guild_ids=[626522675224772658])
    async def agecalc(self, ctx: ApplicationContext, age: AgeConverter):
        await ctx.defer(ephemeral=True)
        await ctx.respond(age, ephemeral=True)

def setup(bot):
    bot.add_cog(AgeCalc(bot))
    logger.info('Loaded AgeCalc')


def teardown(bot):
    bot.remove_cog(AgeCalc(bot))
    logger.info('Unloaded AgeCalc')
