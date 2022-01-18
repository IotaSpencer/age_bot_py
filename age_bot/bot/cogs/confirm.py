import discord
from discord.ext import commands
import logging


class Confirm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx, *, code_string: str):
        # TODO: allow ```code```
        ctx.reply(eval(code_string))


def setup(bot):
    bot.add_cog(Confirm(bot))
    logging.info('Loaded Owner')


def teardown(bot):
    bot.remove_cog(Confirm(bot))
    logging.info('Unloaded Owner')
