# built-ins(?)
import os.path
from pathlib import Path
import asyncio

# (3rd party)
import yaml as YAML
import discord
from discord.ext import bridge
import discord.ext.commands as commands

# local import
from .bot import ProdBot, DevBot
from ..config import Configs
from ..logger import logger


async def start() -> object:
    """

    :rtype: object
    """
    token = Configs.config.bot.token
    env = Configs.config.env.env
    bot = {}
    if env == 'prod':
        bot = ProdBot()
        bot.disable_sending = False

    elif env == 'dev':
        bot = DevBot(intents=discord.Intents.all())
        bot.disable_sending = True
        bot.load_extension('jishaku')

    # Load Jishaku
    bot.load_extension('age_bot.bot.cogs.extensions')
    bot.load_extension('age_bot.bot.cogs.admin')
    bot.load_extension('age_bot.bot.cogs.confirm')
    bot.load_extension('age_bot.bot.cogs.fun')
    bot.load_extension('age_bot.bot.cogs.owner')
    bot.load_extension('age_bot.bot.cogs.id_stuff')
    bot.load_extension('age_bot.bot.cogs.hello')
    bot.load_extension('age_bot.bot.cogs.bad_hello')
    bot.load_extension('age_bot.bot.cogs.join_message')
    bot.load_extension('age_bot.bot.cogs.age_calc')
    bot.load_extension('age_bot.bot.cogs.purge_users')

    await bot.start(token)
