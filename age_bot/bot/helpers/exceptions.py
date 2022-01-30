from discord.ext.commands import CommandError, CheckFailure


class NoAttachmentError(CheckFailure):
    pass


class TooManyAttachmentError(CheckFailure):
    pass
