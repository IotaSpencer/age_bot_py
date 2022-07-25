# built-in

# 3rd party
from discord.ext.commands import Cog, command

# local
from age_bot.loggers import logger


class Admin(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.admin'

    @command()
    async def adminping(self, ctx):
        ctx.reply("Pong! %sms" % ctx.bot.latency)


def setup(bot):
    bot.add_cog(Admin(bot))
    logger.info('Loaded Admin')


def teardown(bot):
    bot.remove_cog(Admin(bot))
    logger.info('Unloaded Admin')
