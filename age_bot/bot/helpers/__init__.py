# built-in

# 3rd party
from typing import Union

from discord import ApplicationContext
from discord.ext.commands import Converter, Context
import arrow as arw
# local

from . import discord, info_embeds, decorators
from . import wait_fors


class AgeConverter(Converter):
    async def convert(self, ctx: Union[ApplicationContext, Context], argument: str):
        now = arw.now()
        d_o_b = arw.get(argument, "DD/MM/YYYY")
        age = ((now.date().year - d_o_b.date().year) * 372 + (now.date().month - d_o_b.date().month) * 31 + (
                now.date().day - d_o_b.date().day)) / 372
        return str(age)
