# built in

import datetime as dt
from itertools import chain
# 3rd party

import discord

from discord.ext.commands import Context, Cog
from discord import Member, Guild, Message, utils, Component

# local imports
from age_bot.config import Configs
from age_bot.logger import logger


class ServerInfo(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def make_db_server_info_embed(self, ctx: Context, guild: Guild):
        adult_role = guild.get_role(Configs.serverdb.servers[str(guild.id)].role)

        adults = adult_role.members
        everyone = guild.members
        everyone_minus_bots = [member for member in everyone if member.bot is False]
        just_bots = [member for member in everyone if member.bot is True]
        channels = guild.channels
        e = discord.Embed(title=f"Server Info: \"{guild.name}\"")
        e.set_thumbnail(url=guild.icon.url)
        e.add_field(name='Adults vs Everyone', value=f"{len(adults)}/{len(everyone_minus_bots)}", inline=True)
        e.add_field(name='Members Count', value=f"{len(everyone_minus_bots)}", inline=True)
        e.add_field(name='Roles Count', value=f"{len(guild.roles)}", inline=False)
        e.add_field(name='Bots Count', value=f"{len(just_bots)}", inline=True)
        e.add_field(name='Channels Count', value=f"{len(channels)}", inline=True)
        e.timestamp = dt.datetime.now()
        footer = [
            f"Guild: {guild.id}",
            f"Requested by {ctx.author}"
        ]
        e.set_footer(text=' \u00b7 '.join(footer))
        return e

    async def make_discord_server_info_embed(self, ctx: Context, guild: Guild):
        e = discord.Embed(title=f"Discord Server Info: \"{guild.name}\"")
        everyone = guild.members
        everyone_minus_bots = [member for member in everyone if member.bot is False]
        just_bots = [member for member in everyone if member.bot is True]
        channels = guild.channels
        e.set_thumbnail(url=guild.icon.url)
        e.add_field(name=f"Total Members:", value=f"{len(guild.members)}", inline=True)
        e.add_field(name=f"Total Members (w/o Bots):", value=f"{len(everyone_minus_bots)}", inline=True)
        e.add_field(name="\u200b", value="\u200b", inline=False)
        e.add_field(name=f"Total Channels:", value=f"{len(channels)}", inline=True)
        e.add_field(name=f"Server Owner:", value=f"{guild.owner}({guild.owner_id})", inline=True)


class ServersInfo(Cog, command_attrs=dict(hidden=True)):
    """Returns discord.Embed lists"""
    async def make_servers_info_embed(self, ctx: Context, guild: Guild):
        """
        :arg ctx Context
        :arg guild Guild
        """
        db_server_embeds = []  # type: list[discord.Embed]
        discord_embeds = []  # type: list[discord.Embed]

        db_servers = [item for item in Configs.serverdb.servers.keys()]
        discord_servers = ctx.bot.guilds

        for server in db_servers:
            e = await ServerInfo(ctx.bot).make_db_server_info_embed(ctx, ctx.bot.get_guild(int(server)))
            db_server_embeds.append(e)

        for item in discord_servers:
            e = await ServerInfo(ctx.bot).make_discord_server_info_embed(ctx, item)
            discord_embeds.append(e)

        return [db_server_embeds, discord_embeds]


def setup(bot):
    bot.add_cog(ServerInfo(bot))
    bot.add_cog(ServersInfo(bot))
    logger.info('Loaded Info Embed Objects')


def teardown(bot):
    bot.remove_cog(ServerInfo(bot))
    bot.remove_cog(ServersInfo(bot))
    logger.info('Unloaded Info Embed Objects')
