# built-in
import asyncio

# 3rd party
import discord
from discord import ApplicationContext, slash_command
from discord.ext import commands, pages, bridge

# local
from age_bot.bot.helpers.discord_helpers import member_distinct
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

    @slash_command()
    async def whoami(self, ctx: ApplicationContext):
        await ctx.respond(ephemeral=True, content=f"Hello {member_distinct(ctx.user)}.\n"
                                                  "My name is 年齢-様 or Nenrei-Sama, or just Nenrei.\n"
                                                  "I'm a bot that helps some server owners verify that their users are as old as they say they are."
                                                  "I do this by receiving your ID+discord tag after you run the slash-command **/verify**"
                                                  "in the '#hello' channel of the servers I share with you.\n"
                                                  "\n"
                                                  "For more information, see one of the following.\n"
                                                  "> * The aforementioned '#hello' channel\n"
                                                  "> * An admin of one of the servers I share with you.\n"
                                                  "> * My owner and developer iotaspencer#0001 or his server.\n"
                                                  ">     https://discord.gg/nBB7K5y -- If this invite becomes invalid, let him know.")

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
