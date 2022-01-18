import discord
from discord.commands import SlashCommandGroup, CommandPermission
from discord.ext import commands
import logging
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def adminping(self, ctx, *, code_string: str):
        ctx.reply("Pong! %sms" % ctx.bot.latency)

def setup(bot):
    bot.add_cog(Admin(bot))
    logging.info('Loaded Admin')

def teardown(bot):
    bot.remove_cog(Admin(bot))
    logging.info('Unloaded Admin')