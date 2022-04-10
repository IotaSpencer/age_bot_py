import discord
from discord.ext.commands import Context
from typing import Union


def author_distinct(ctx: Context):
    user = ctx.author
    return user.name + user.discriminator


def member_distinct(member: discord.Member):
    return "{}#{}".format(member.name, member.discriminator)
