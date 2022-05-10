# built-in

# 3rd Party
from typing import Union

import discord
from discord.ext import commands, bridge
from discord import Member, Message

# local imports
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
from discord.ext.commands import guild_only

from age_bot.bot.helpers.discord import *
from ...config import Configs
from age_bot.logger import logger


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.hello'

    @guild_only()
    @bridge.bridge_command()
    async def hello(self, ctx):
        await ctx.reply(
            f"Hello, {member_distinct(ctx.author)}, in order to post or read {ctx.guild.name} messages you must be a certain role as well as "
            f"submitted a form of ID with the server in question."
            f"\n\n"
            f"Please see #id-example and #upload-example for examples on how to upload and format your message.\n"
            f"Do not worry about the '&verify 626...."
            f"\n\n"
            f"For {ctx.guild.name} that role is "
            f"{ctx.guild.get_role(Configs.serverdb.servers[str(ctx.guild.id)].role)} "
            f"\n\n"
            f"To do so, please run the **command** /verify"
            f""
        )

    @commands.has_any_role('Server Helpers', 'Discord moderator', 'Mods')
    @bridge.bridge_command(signature='')
    async def fhello(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], user: discord.Member):
        if is_slash_command(ctx):
            ctx.defer()
        else:
            pass
        usr = ctx.guild.get_member_named(user)  # type: Member
        adult_role = ctx.guild.get_role(Configs.serverdb.servers[str(ctx.guild.id)].role)
        await usr.send(
            f"Hello, {member_distinct(usr)}, in order to post or read {ctx.guild.name} messages you must be a "
            f"certain role as well as "
            f"submitted a form of ID with the server in question."
            f"\n\n"
            f"Please see #id-example and #upload-example for examples on how to upload and format your message.\n"

            f"\n\n"
            f"For {ctx.guild.name} that role is "
            f"{adult_role} "
            f"\n\n"
            f"To do so, please run the command /verify in #hello"
        )

    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        orig_msg = msg
        if msg.guild and msg.channel:
            if msg.channel.name == 'hello':
                if msg.channel_mentions:
                    if msg.channel_mentions[0].name == 'hello':
                        shame_msg = await msg.reply(content="The command is '&hello' nothing else"
                                                            "As per our above rules, as you mentioned the channel, "
                                                            "you shall be named and shamed.")
                        if find_shamed(msg.guild.text_channels):
                            shame_channel = find_shamed(msg.guild.text_channels)
                            shamed_user = msg.author
                            shamed_time = msg.created_at
                            await shame_channel.send(
                                "{shamed_user} mentioned '#hello' in #hello at {shamed_time}".format(
                                    shamed_user=member_distinct(shamed_user), shamed_time=shamed_time))
                            await shame_msg.delete(delay=10)
                            await msg.delete(delay=10)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass


def setup(bot):
    bot.add_cog(Hello(bot))
    logger.info('Loaded Hello')


def teardown(bot):
    bot.remove_cog(Hello(bot))
    logger.info('Unloaded Hello')
