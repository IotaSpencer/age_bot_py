import discord
from discord.ext import commands
import logging
import age_bot.bot.helpers.discord as dhelpers


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, *, code_string: str):
        ctx.reply("""
        Hello, %s, in order to post or read %s messages you must be a certain role as well as submitted a form of ID with the server in question.
For %s that role is Adult
To do so, please send me a picture of your ID with everything but your 'date of birth' blacked out along with some sort of Discord™ proof (Your account page with the email blacked out or a handwritten Discord™ tag) 

  For you that would be %s
  When you do so, attach this string below to the picture as a caption.

  &verify %i
        """ % ctx.author.name, ctx.guild.name, ctx.guild.name, dhelpers.author_distinct(ctx))


def setup(bot):
    bot.add_cog(Hello(bot))
    logging.info('Loaded Owner')


def teardown(bot):
    bot.remove_cog(Hello(bot))
    logging.info('Unloaded Owner')
