# built-in
from typing import Union
# 3rd party
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
# local
from .discord import *
from ...exceptions import ConfirmPermError, HelperPermError

async def confirmable_check(ctx: BridgeExtContext):
    if has_server_confirm_role(ctx.guild, ctx.user):
        return True
    else:
        raise ConfirmPermError

async def helper_check(ctx: Context):
    if has_server_helper_role(ctx.guild, ctx.user):
        return True
    else:
        raise HelperPermError