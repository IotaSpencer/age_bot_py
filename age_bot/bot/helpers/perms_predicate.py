# built-in
from typing import Union
# 3rd party
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
# local
from .discord import *
from discord import commands
from discord.ext.commands import check
from ...exceptions import ConfirmPermError, HelperPermError

def confirmable_check():
    def predicate(ctx):
        if has_server_confirm_role(ctx.guild, ctx.author):
            return True
        else:
            raise ConfirmPermError
    return check(predicate)

def helper_check():
    def predicate(ctx):
        if has_server_helper_role(ctx.guild, ctx.author):
            return True
        else:
            raise HelperPermError
    return check(predicate)