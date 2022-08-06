# built-in
from typing import Union
import inspect
from pathlib import Path
import re
# 3rd Party
import discord
from discord.ext import commands, bridge
from discord import Member, Message
# local imports
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
from discord.ext.commands import guild_only
from age_bot.bot.helpers.discord_helpers import *
from age_bot.bot.helpers.perms_predicate import *
from ...config import Configs
from age_bot.loggers import logger


class Hello(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.hello'

    @guild_only()
    @bridge.bridge_command()
    async def hello(self, ctx):
        await ctx.defer(ephemeral=True) if ctx.__class__.__name__ in ['ApplicationContext', 'BridgeApplicationContext'] else await ctx.defer()
        if check_if_tester_or_main_bot(ctx, self.bot):
            await ctx.reply(
                f"Hello, {member_distinct(ctx.author)}, in order to post or read {ctx.guild.name} messages you must be a certain role as well as "
                f"submitted a form of ID with the server in question."
                f"\n\n"
                f"Please see #id-example for examples on how and format your message."
                f"\n\n"
                f"For {ctx.guild.name} that role is "
                f"{get_adult_role(ctx)} "
                f"\n\n"
                f"To do so, please run the **command** /verify, and I will message you with further instructions. "
                f"Also see the #slash-commands channel for info on how to use slash commands."
                f"",
            )

    @helper_check()
    @discord.commands.default_permissions(manage_server=True)
    @bridge.bridge_command(signature='')
    async def fhello(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], user: discord.Member):
        if is_slash_command(ctx):
            ctx.defer(ephemeral=True)
        else:
            pass
        usr = ctx.guild.get_member_named(user)  # type: Member
        adult_role = get_adult_role(ctx)
        await usr.send(
            f"Hello, {user_distinct(usr)}, in order to post or read {ctx.guild.name} messages you must be a "
            f"certain role as well as "
            f"submitted a form of ID with the server in question."
            f"\n\n"
            f"Please see #id-example for examples on how to upload and format your message.\n"

            f"\n\n"
            f"For {ctx.guild.name} that role is {adult_role} "
            f"\n\n"
            f"To do so, please run the command /verify in #hello, and I will message you with further instructions. "
            f"Also see the #slash-commands channel for info on how to use slash commands."
        )

    @discord.Cog.listener()
    async def on_message(self, msg: Message):
        if check_if_tester_or_main_bot(msg, self.bot):
            orig_msg = msg
            if msg.guild and msg.channel: # check if message is in a guild and has a channel
                if msg.channel.name == 'hello': # check if message is in the hello channel
                    if message.author.bot is not True and \
                        re.search("^([!@$/]?(verify|hello))$", message.content, re.IGNORECASE) and \
                            message.channel.name == 'hello':
                        try:
                            our_message = await message.author.send(
                                f"Hello, {message.author}, in order to post or read {message.guild} messages you must be a certain"
                                f" role as well as submitted a form of ID with the server in question. For {message.guild} "
                                f"that role is **{get_adult_role(ctx)}** "
                                f"\n\n"
                                f"To do so.. please run the **command** /verify in #hello and I will message you with further "
                                f"instructions. Also see the #slash-commands channel for info on how to use slash commands."
                                f"\n\n"
                                f"You are receiving this message because you messaged #{message.channel} a message that triggered "
                                f"me.\n "
                                f"Your message will now be deleted since the message holds no purpose in #{message.channel}."
                                f"\n\n"
                                f"You may ask questions about the process in #{message.channel} but other than that, "
                                f"non-complying questions or messages will be deleted.")
                            await message.delete(delay=0)
                            await our_message.delete(delay=120)
                        except Forbidden:
                            hello_channel = Configs.sdb.servers[str(message.guild.id)].hello_channel
                            hello_chan = await message.guild.fetch_channel(hello_channel)
                            await hello_chan.send(
                                f"Hey {message.author.mention}, I can't seem to send you a message, please make sure you "
                                f"have accept messages from server members ticked.", delete_after=120)
                    elif msg.channel_mentions and msg.author.bot is not True: # Don't react to bots
                        if msg.channel_mentions[0].name == 'hello':
                            shame_msg = await msg.reply(content="The command is '/hello' nothing else"
                                                                "As per our above rules, as you mentioned the channel, "
                                                                "you shall be named and shamed.")
                            if find_shamed(msg.guild.text_channels):
                                shame_channel = find_shamed(msg.guild.text_channels)
                                shamed_user = msg.author
                                shamed_time = msg.created_at
                                await shame_channel.send(
                                    "{shamed_user} mentioned '#hello' in #hello at {shamed_time}".format(
                                        shamed_user=member_distinct(shamed_user), shamed_time=shamed_time))
                                await shame_msg.delete(delay=20)
                                await msg.delete(delay=20)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            logger.info(f"dev env active, ignoring {inspect.stack()[0][3]} in {Path(__file__).stem}")
            pass

def setup(bot):
    bot.add_cog(Hello(bot))
    logger.info('Loaded Hello')


def teardown(bot):
    bot.remove_cog(Hello(bot))
    logger.info('Unloaded Hello')
