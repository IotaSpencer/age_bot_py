# built-in
import asyncio

# 3rd party
import discord
from discord.ext import commands, pages, bridge

# local
from discord.ext.commands import Context

from age_bot.loggers import logger
from age_bot.config import Configs
from age_bot.bot.helpers.info_embeds import *


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.fun'

    @bridge.bridge_command()
    async def ping(self, ctx: Context):
        await ctx.reply("Pong %sms" % ctx.bot.latency)

    @commands.guild_only()
    @commands.is_owner()
    @commands.command()
    async def serverinfo(self, ctx: Context):
        waiting = await ctx.reply("Grabbing server info..")
        async with ctx.channel.typing():
            await asyncio.sleep(2)
            embed = await ServerInfo(ctx.bot).make_db_server_info_embed(ctx, ctx.guild)
            await ctx.reply(embed=embed)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def serversinfo(self, ctx: Context):
        waiting = await ctx.reply("Grabbing all servers' info..")
        async with ctx.channel.typing():
            await asyncio.sleep(2)
            server_pages = await ServersInfo(ctx.bot).make_servers_pages(ctx)
            paginator = pages.Paginator(
                pages=server_pages,
                show_disabled=True,
                show_indicator=True,
                use_default_buttons=True,
                loop_pages=True,
            )
            await paginator.send(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
    logger.info('Loaded Fun')


def teardown(bot):
    bot.remove_cog(Fun(bot))
    logger.info('Unloaded Fun')
