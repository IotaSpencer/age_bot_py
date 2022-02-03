# built-in

# 3rd party
import discord
from discord.commands import SlashCommandGroup, CommandPermission
from discord.ext import commands

# local
from age_bot.logger import logger


class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.admin'
    
    
    @commands.command()
    async def adminping(self, ctx, *, code_string: str):
        ctx.reply("Pong! %sms" % ctx.bot.latency)

def setup(bot):
    bot.add_cog(Admin(bot))
    logger.info('Loaded Admin')

def teardown(bot):
    bot.remove_cog(Admin(bot))
    logger.info('Unloaded Admin')
