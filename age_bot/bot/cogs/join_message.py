# built-in
import asyncio

# 3rd party
import discord
from discord.ext import commands
from discord import Member

# local
from age_bot.logger import logger


class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.join_message'

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        asyncio.sleep(60)
        member.send(
            f"Hello, {message.author}, in order to post or read {message.guild} messages you must be a certain"
            f" role as well as submitted a form of ID with the server in question. For {message.guild} "
            f"that role is **{message.guild.get_role(Configs.serverdb.servers[str(message.guild.id)].role).name}**"
            f"\n\n"
            f"To do so.. please run the command /verify in #hello and I will message you with further instructions."
            f"\n\n"
            f"You may ask questions about the process in #{message.channel} but other than that, "
            f"non-complying questions or messages will be deleted."
        )



def setup(bot):
    bot.add_cog(JoinMessage(bot))
    logger.info('Loaded JoinMessage')

def teardown(bot):
    bot.remove_cog(JoinMessage(bot))
    logger.info('Unloaded JoinMessage')
