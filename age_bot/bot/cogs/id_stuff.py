import discord
from discord import Message
from discord.ext import commands
import logging


class IDStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_attachment():
        def predicate(ctx):
            return ctx.message.attachments.len() == 1
        return commands.check(predicate)

    @commands.command()
    @has_attachment
    async def verify(self, ctx, guild: discord.Guild):
        if guild:
            if ctx.message.attachments:
                if ctx.message.attachments.len() == 1:

    @verify.error
    async def verify_error(ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Server ID is needed for verification')
            mutual_guilds = ctx.author.mutual_guilds
            guild_string = ''
            for guild in mutual_guilds:
                guild_string.append("{0}({1})".format(guild.name, guild.id))
            await ctx.send("Applicable Server IDs are {0}".format(guild_string))
            await ctx.send("Send your ID, with one of the server IDs listed, the server ID is the number in parentheses.")

def setup(bot):
    bot.add_cog(IDStuff(bot))
    logging.info('Loaded IDStuff')


def teardown(bot):
    bot.remove_cog(IDStuff(bot))
    logging.info('Unloaded IDStuff')
