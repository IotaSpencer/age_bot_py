# built-in
import inspect
import re
from pathlib import Path
from typing import Union

# 3rd Party
import discord
from discord.ext import bridge
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
from discord import Forbidden, Message
from discord.ext.commands import guild_only

# local imports
from age_bot.loggers import logger
from age_bot.bot.helpers.discord_helpers import check_if_tester_or_main_bot, find_shamed, get_adult_role, is_slash_command, \
    member_distinct, \
    user_distinct
from age_bot.bot.helpers.perms_predicate import helper_check
from age_bot.config import Configs


class Hello(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.hello'

    @guild_only()
    @bridge.bridge_command()
    async def hello(self, ctx):
        await ctx.defer(ephemeral=True) if ctx.__class__.__name__ in ['ApplicationContext',
                                                                      'BridgeApplicationContext'] else await ctx.defer()
        if check_if_tester_or_main_bot(ctx, self.bot):
            await ctx.reply(
                f"Hello, {member_distinct(ctx.author)}, in order to post or read {ctx.guild.name} messages you must be a certain role as well as "
                f"submitted a form of ID+Discord-tag with the server in question."
                f"\n\n"
                f"Please see #id-example for examples on how to prep your photo."
                f"\n\n"
                f"For {ctx.guild.name} that role is "
                f"{get_adult_role(ctx)} "
                f"\n\n"
                f"To do so, please run the **command** /verify, and I will message you with further instructions. "
                f"Also see the #slash-commands channel for info on how to use slash commands."
                f"",
            )

    @helper_check()
    @discord.commands.default_permissions(manage_guild=True)
    @bridge.bridge_command(signature='')
    async def fhello(self, ctx: Union[BridgeApplicationContext, BridgeExtContext], user: discord.Member):
        if is_slash_command(ctx):
            ctx.defer(ephemeral=True)
        else:
            pass
        adult_role = get_adult_role(ctx)
        await user.send(
            f"Hello, {user_distinct(user)}, in order to post or read {ctx.guild.name} messages you must be a "
            f"certain role as well as "
            f"submitted a form of ID+Discord-tag with the server in question."
            f"\n\n"
            f"Please see #id-example for examples on how to prep your photo.\n"
            f"\n\n"
            f"For {ctx.guild.name} that role is {adult_role} "
            f"\n\n"
            f"To do so, please run the command **/verify** in #hello, and I will message you with further instructions. "
            f"Also see the #slash-commands channel for info on how to use slash commands."
        )
        await ctx.respond(f"**/hello** forced on {member_distinct(user)}")

    @discord.Cog.listener()
    async def on_message(self, msg: Message):
        if check_if_tester_or_main_bot(msg, self.bot):
            if msg.guild and msg.channel:  # check if message is in a guild and has a channel
                if msg.channel.name == 'hello':  # check if message is in the hello channel
                    if msg.author.bot is not True and \
                            re.search("^([!@$/]?(verify|hello))$", msg.content, re.IGNORECASE) and \
                            msg.channel.name == 'hello':
                        try:
                            our_message = await msg.author.send(
                                f"Hello, {msg.author}, in order to post or read {msg.guild} messages you must be a certain"
                                f" role as well as submitted a form of ID with the server in question. For {msg.guild} "
                                f"that role is **{get_adult_role(msg)}** "
                                f"\n\n"
                                f"To do so.. please run the **slash-command** /verify in #hello and I will message you with further "
                                f"instructions. Also see the #slash-commands channel for info on how to use slash commands."
                                f"\n\n"
                                f"You are receiving this message because you messaged #{msg.channel} a message that triggered "
                                f"me.\n "
                                f"Your message will now be deleted since the message holds no purpose in #{msg.channel}."
                                f"\n\n"
                                f"You may ask questions about the process in #{msg.channel} but other than that, "
                                f"non-complying questions or messages will be deleted.")
                            await msg.delete(delay=120)
                            await our_message.delete(delay=120)
                        except Forbidden:
                            hello_channel = Configs.sdb.servers[str(msg.guild.id)].hello_channel
                            hello_chan = await msg.guild.fetch_channel(hello_channel)
                            await hello_chan.send(
                                f"Hey {msg.author.mention}, I can't seem to send you a message, please make sure you "
                                f"have accept messages from server members ticked.", delete_after=120)
                    elif msg.channel_mentions and msg.author.bot is not True:  # Don't react to bots
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
