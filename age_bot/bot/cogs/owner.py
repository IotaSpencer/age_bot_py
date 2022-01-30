# built-in function
import re

# 3rd party
import discord
from discord.ext import commands

# local
from age_bot.logger import logger


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.owner'

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code_string: str):
        # TODO: allow ```code```
        async with ctx.channel.typing():
            if ctx.message.content.startswith(
                    '{prefix}eval ```python'.format(prefix=ctx.bot.command_prefix)) and ctx.message.content.endswith(
                    '```'):
                eval(re.sub(r'''\^eval ```python\n(.*)\n?```''', '\\1', ctx.message.content, re.S))

            elif len(ctx.message.attachments) != 0:
                pass
            else:
                await ctx.reply(eval(code_string))

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.close()
        await ctx.bot.loop.close()


def setup(bot):
    bot.add_cog(Owner(bot))
    logger.info('Loaded Owner')


def teardown(bot):
    bot.remove_cog(Owner(bot))
    logger.info('Unloaded Owner')
