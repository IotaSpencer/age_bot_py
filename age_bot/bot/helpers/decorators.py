from age_bot.bot.helpers.exceptions import NoAttachmentError, TooManyAttachmentError
from age_bot.logger import logger
from discord.ext.commands import Context
from discord.ext import commands
from age_bot.config import Config, ServerDB

class Decorators:
    """Decorators for checks and bot things"""
    @classmethod
    def is_other_bot_online(self):
        def predicate(ctx: Context):
            return ctx.guild.get_member(719736166819037314).status == 'online'

    @classmethod
    def is_valid_server_in_db(self):
        def predicate(ctx):
            in_discord = False
            in_db = False
            guild_id = ctx.message.content.split(' ')[1]  # may not be valid guild ID
            if ctx.get_guild("{}".format(guild_id)):  # see if exists on discord
                in_discord = True
            else:
                pass
            if guild_id in ServerDB.servers.to_dict().keys():
                in_db = True
            else:
                pass

            return in_db and in_discord

        return commands.check(predicate)
