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

    @commands.command()
    @slash_command(name='agecalc', guild_ids=[626522675224772658])
    async def agecalc(self, ctx: Union[Context, ApplicationContext], age: AgeConverter):
        ctx.respond(age, ephemeral=True)
