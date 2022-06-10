# built-in
import re

# 3rd party
import discord
from discord.ext import commands
from discord import Message

# local
from age_bot.bot.helpers.discord import *
from age_bot.logger import logger
from age_bot.config import Configs
from age_bot.bot.helpers.decorators import *

class BadHello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.bad_hello'

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if check_if_tester_or_main_bot(message, self.bot):
            if message.author.bot is not True:
                if re.search("^([!@$/]?(verify|hello)\S+)$",
                             message.content, re.IGNORECASE) and message.channel.name == 'hello':
                    our_message = await message.author.send(
                        f"Hello, {message.author}, in order to post or read {message.guild} messages you must be a certain"
                        f" role as well as submitted a form of ID with the server in question. For {message.guild} "
                        f"that role is **{message.guild.get_role(Configs.serverdb.servers[str(message.guild.id)].role).name}** "
                        f"\n\n"
                        f"To do so.. please run the command /verify in #hello and I will message you with further "
                        f"instructions. "
                        f"\n\n"
                        f"You are receiving this message because you messaged #{message.channel} a message that triggered "
                        f"me.\n "
                        f"Your message will now be deleted since the message holds no purpose in #{message.channel}."
                        f"\n\n"
                        f"You may ask questions about the process in #{message.channel} but other than that, "
                        f"non-complying questions or messages will be deleted.")
                    await message.delete(delay=0)
                    await our_message.delete(delay=120)


def setup(bot: discord.Bot):
    bot.add_cog(BadHello(bot))
    logger.info('Loaded BadHello')


def teardown(bot):
    bot.remove_cog(BadHello(bot))
    logger.info('Unloaded BadHello')
