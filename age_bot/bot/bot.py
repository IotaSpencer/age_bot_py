# built-in
# 3rd party
import discord
import omegaconf.errors
from discord.ext import bridge
import arrow as arw
# local
from ..config import Configs
from ..logger import logger
from ..bot.helpers.discord import *
from ..bot.helpers.decorators import *


class Bot(bridge.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        token = Configs.config.bot.token
        prefix = Configs.config.bot.prefix
        db_guilds = Configs.serverdb.servers.keys()
        debug_guilds = [server for server in db_guilds]
        self.command_prefix = prefix
        try:
            self.owner_ids = Configs.config.bot.owners
            puts(self.owner_ids)
        except omegaconf.errors.ConfigAttributeError:
            self.owner_ids = [Configs.config.bot.owner]
        self.debug_guilds = debug_guilds
        self.max_messages = 10000
        self.status = discord.Status.online


class DevBot(Bot):
    def __init__(self, **options):
        super().__init__(**options)

    async def on_ready(self):
        logger.info(f"Bot is online and ready! Name is {self.user}")
        app = await self.application_info()
        app_name = app.name
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"{app_name}"
        ), status=discord.Status.online)


class ProdBot(Bot):
    def __init__(self, **options):
        super().__init__(**options)
