# built-in

# 3rd party
from typing import Union

from discord import ApplicationContext
from discord.ext.commands import Converter, Context
import arrow as arw
# local

from . import discord, info_embeds, decorators
from . import wait_fors


def calculate_age(dob):
    today = date.today()
    born = arw.get(dob, 'DD/MM/YYYY')
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
