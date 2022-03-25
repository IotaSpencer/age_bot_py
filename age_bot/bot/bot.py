# built-ins(?)
import os.path
from pathlib import Path
import asyncio

# (3rd party)
import yaml as YAML
import discord
import discord.ext.commands as commands

# local import
from ..config import Configs
from ..logger import logger


async def start() -> object:
    """

    :rtype: object
    """
    token = Configs.config.bot.token
    prefix = Configs.config.bot.prefix
    bot = commands.Bot(
        owner_id=234093061045616642,
        debug_guilds=[],
        command_prefix=prefix,
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
        activity=discord.Activity(name="the interwebs", type=discord.ActivityType.watching),

    )
    # todo: either use config files to retrieve the environment or use a platform+user checker


    # Load Jishaku
    bot.load_extension('jishaku')
    # work out cogs then uncomment
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
    bot.load_extension('age_bot.bot.helpers.info_embeds')

    @bot.event
    async def on_ready():
        logger.info(f"Bot is online and ready! Name is {bot.user}")

    await bot.start(token)





class Bot:
    pass
