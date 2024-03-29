# built-in
import asyncio
from pathlib import Path
import inspect
# 3rd party
import discord
from discord.errors import Forbidden
from discord.ext import commands, bridge
from discord import Member, TextChannel

# local
from age_bot.bot.helpers.decorators import *
from age_bot.bot.helpers.discord_helpers import *
from age_bot.loggers import logger
from age_bot.config import Configs


class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.join_message'

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        if check_if_tester_or_main_bot(member, self.bot):
            await asyncio.sleep(5)
            try:
                await member.send(
                    f"Hello, {member}, in order to post or read {member.guild} messages you must be a certain"
                    f" role as well as submitted a form of ID with the server in question. For {member.guild} "
                    f"that role is **{member.guild.get_role(Configs.sdb.servers[str(member.guild.id)].role).name}**"
                    f"\n\n"
                    f"To do so.. please run the **command** /verify in #hello and I will message you with further "
                    f"instructions. Also see the #slash-commands channel for info on how to use slash commands."
                    f"\n\n"
                    f"You may ask questions about the process in #hello but other than that, "
                    f"non-complying questions or messages will be deleted."
                )
            except Forbidden:
                hello_channel = Configs.sdb.servers[str(member.guild.id)].hello_channel
                hello_chan = await member.guild.fetch_channel(hello_channel)  # type: TextChannel
                await hello_chan.send(f"Hey {member.mention}, I can't seem to send you a message, please make sure you "
                                      f"have accept messages from server members ticked.", delete_after=120)

        else:
            logger.info(f"dev env active, ignoring {inspect.stack()[0][3]} in {Path(__file__).stem}")

def setup(bot):
    bot.add_cog(JoinMessage(bot))
    logger.info('Loaded JoinMessage')


def teardown(bot):
    bot.remove_cog(JoinMessage(bot))
    logger.info('Unloaded JoinMessage')
