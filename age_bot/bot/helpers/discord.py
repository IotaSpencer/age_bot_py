import discord
from discord.ext.commands import Context
from typing import Union

async def author_distinct(ctx: Context):
    user = ctx.author
    return user.name + user.discriminator
