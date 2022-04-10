import omegaconf.errors
from discord.ext.commands import CommandError, CheckFailure


class NoAttachmentError(CheckFailure):
    pass


class TooManyAttachmentError(CheckFailure):
    pass


class NoGuildInContextError(CheckFailure):
    pass


class GuildNotInDBError(omegaconf.errors.ConfigKeyError):
    pass
