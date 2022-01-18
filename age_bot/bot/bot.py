# built-ins(?)
import os.path
from pathlib import Path
import asyncio

# (3rd party)
import yaml as YAML
import discord
import discord.ext.commands as commands
import logging

# local import
from ..config import Config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
import age_bot.bot.cogs

async def start():
    token = Config.bot.token
    bot = commands.Bot(extensions=[
        'slash',
        'commands_v2',
    ],
        debug_guild=626522675224772658,
        owner_id=234093061045616642,
        command_prefix='^',
        max_messages=10000,
        intents=discord.Intents(
            bans=True,
            dm_messages=True,
            dm_reactions=True,
            dm_typing=True,
            emojis=True,
            guild_messages=True,
            guild_reactions=True,
            guild_typing=True,
            guilds=True,
            integrations=True,
            invites=True,
            members=True,
            messages=True,
            presences=True,
            reactions=True,
            typing=True,
            webhooks=True),
        status=discord.Status.online,
        activity=discord.Activity(name="the interwebs",type=discord.ActivityType.watching),

    )

    # work out cogs then uncomment
    bot.load_extension('age_bot.bot.cogs.admin')
    bot.load_extension('age_bot.bot.cogs.fun')
    bot.load_extension('age_bot.bot.cogs.owner')
    bot.load_extension('age_bot.bot.cogs.id_stuff')
    await bot.start(token)


class Bot:
    pass
