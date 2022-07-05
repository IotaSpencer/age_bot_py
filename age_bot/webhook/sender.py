import discord
import asyncio
import aiohttp

from age_bot.config import Configs
from age_bot.webhook.bot_url import get_bot_url

async def send(bot_name, logObj):
    async with aiohttp.ClientSession() as session:
        url = get_bot_url(bot_name)
        session.headers.add('Content-Type', 'application/json')
        await session.post(url, json=logObj)