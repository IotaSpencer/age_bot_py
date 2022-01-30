# built-in function
import re

# 3rd party
import discord
from discord.ext import commands

# local
from age_bot.logger import logger


class Extensions(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.extensions'

    @commands.group(case_insensitive=True)
    async def ext(self, ctx):
        pass

    @ext.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        ctx.bot.load_extension(extension)
        await ctx.reply('Loaded {}'.format(extension))

    @ext.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        ctx.bot.unload_extension(extension)
        await ctx.reply('Unloaded {}'.format(extension))

    @ext.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        ctx.bot.reload_extension(extension)
        await ctx.reply('Reloaded {}'.format(extension))

    @commands.group()
    @commands.is_owner()
    async def cogs(self, ctx):
        pass

    @cogs.command()
    async def reload(self, ctx):
        for cog_name, cog_class in ctx.bot.cogs.copy().items():
            if cog_class.ext_path != 'age_bot.bot.cogs.extensions':
                ctx.bot.reload_extension(cog_class.ext_path)
        await ctx.reply("Reloaded all cogs.")
        await ctx.botregister_commands


def setup(bot):
    bot.add_cog(Extensions(bot))
    logger.info('Loaded Extensions')


def teardown(bot):
    bot.remove_cog(Extensions(bot))
    logger.info('Unloaded Extensions')
