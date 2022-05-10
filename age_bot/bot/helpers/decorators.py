from discord.ext.commands import Context
from discord.ext import commands
from age_bot.config import Configs

# Decorator version
def is_other_bot_offline() -> bool:
    def predicate(ctx: Context):
        return ctx.guild.get_member(719736166819037314).status != 'online'

    return commands.check(predicate)

# Non-Decorator
async def is_other_bot_offline2(self, ctx: Context) -> bool:
    return await ctx.get_or_fetch_user(719736166819037314).status != 'online'


def is_valid_server_in_db(self):
    def predicate(ctx):
        in_discord = False
        in_db = False
        guild_id = ctx.message.content.split(' ')[1]  # may not be valid guild ID
        if ctx.get_guild("{}".format(guild_id)):  # see if exists on discord
            in_discord = True
        else:
            pass
        if guild_id in Configs.serverdb.servers.keys():
            in_db = True
        else:
            pass

        return in_db and in_discord

    return commands.check(predicate)
