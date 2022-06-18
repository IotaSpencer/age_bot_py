# built-in

# 3rd party
from discord.ext.commands import Cog, command

# local
from age_bot.logger import logger
from age_bot.bot.helpers.discord import *


class DevBotCog(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.ext_path = 'age_bot.bot.cogs.devbotcog'

    @Cog.listener()
    async def self_is_dev(self, message):
        """
        Since this only loaded on the DevBot, we don't need to check if it is the dev bot
        """
        if check_if_tester_or_main_bot(message, self.bot):
            pass # If they are a tester, act as usual
        else: # We're devbot, and user is not a tester
            await reply_self_is_dev2(message, self.bot)

        # then do things pertaining to devbot
        # like telling people to use the main bot

def setup(bot):
    bot.add_cog(DevBotCog(bot))
    logger.info('Loaded DevBotCog')


def teardown(bot):
    bot.remove_cog(DevBotCog(bot))
    logger.info('Unloaded DevBotCog')
