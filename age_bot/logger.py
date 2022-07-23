import logging, datetime, sys, json_logging, flask, colorlog, discord
from asyncio.subprocess import STDOUT
from logging_disgram.logging_handlers import DiscordHandler, TelegramHandler
import logging.config
from age_bot.config import Configs
from logging import LogRecord
import os

def escape_markdown(text, *, as_needed=False, ignore_links=True):
    r"""A helper function that escapes Discord's markdown.

    Parameters
    -----------
    text: :class:`str`
        The text to escape markdown from.
    as_needed: :class:`bool`
        Whether to escape the markdown characters as needed. This
        means that it does not escape extraneous characters if it's
        not necessary, e.g. ``**hello**`` is escaped into ``\*\*hello**``
        instead of ``\*\*hello\*\*``. Note however that this can open
        you up to some clever syntax abuse. Defaults to ``False``.
    ignore_links: :class:`bool`
        Whether to leave links alone when escaping markdown. For example,
        if a URL in the text contains characters such as ``_`` then it will
        be left alone. This option is not supported with ``as_needed``.
        Defaults to ``True``.

    Returns
    --------
    :class:`str`
        The text with the markdown special characters escaped with a slash.
    """

    if not as_needed:
        url_regex = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'
        def replacement(match):
            groupdict = match.groupdict()
            is_url = groupdict.get('url')
            if is_url:
                return is_url
            return '\\' + groupdict['markdown']

        regex = r'(?P<markdown>[_\\~|\*`]|%s)' % _MARKDOWN_ESCAPE_COMMON
        if ignore_links:
            regex = '(?:%s|%s)' % (url_regex, regex)
        return re.sub(regex, replacement, text)
    else:
        text = re.sub(r'\\', r'\\\\', text)
        return _MARKDOWN_ESCAPE_REGEX.sub(r'\\\1', text)

class EscapeFilenameforDiscord(logging.Filter):
    def filter(self, record):
        if record.filename:

            record.filename = escape_markdown(record.filename)
        return True

class LevelFilter(logging.Filter):
    """
    This is a filter which changes the levelname to that of its Initial letter

    """

    def filter(self, record):
        record.level_initial = record.levelname[0]
        return True


secondary_log_colors = {
    'message': {
        'E': 'red',
        'C': 'red',
        'W': 'yellow',
        'I': 'green',
        'D': 'blue',
    },
    'name': {
        'E': 'red',
        'C': 'red',
        'W': 'yellow',
        'I': 'green',
        'D': 'blue',
    },
    'file': {
        'E': 'red',
        'C': 'red',
        'W': 'yellow',
        'I': 'green',
        'D': 'blue',
    }
}
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
    'D': 'cyan',
    'I': 'green',
    'W': 'yellow',
    'E': 'red',
    'C': 'red,bg_white'
}

class EmojiFilter(logging.Filter):
    """This is a filter that replaces levelname with emojis"""

    def filter(self, record: LogRecord) -> bool:
        level = record.levelname
        levels = {
            'WARNING': '⚠',
            'ERROR': '‼',
            'CRITICAL': '☠',
            'DEBUG': '❓',
            'INFO': '✅'
        }
        try:
            record.level_emoji = levels[level]
            return True
        except:
            return False

handlers = ['telegram_handler', 'file_handler', 'stream_handler', 'discord_handler']
logging.config.dictConfig({
    'version': 1,
    'filters': {
        'level_filter': {
            '()': LevelFilter,
        },
        'emoji_filter': {
            '()': EmojiFilter,

        },
        'escape_markdown': {
            '()': EscapeFilenameforDiscord,
        }
    },
    'formatters': {
        'telegram_formatter': {
            'format': "<b>%(levelname)s</b> <b>%(name)s</b> <b>%(asctime)s</b>\n"
                      "     <b>%(filename)s</b> <b>%(funcName)s</b> <b>%(lineno)s</b>\n"
                      "         ```%(message)s```",
            #'style': '{'
        },
        'discord_format': {
            'format':"{level_emoji}->**{levelname}** \n**Logger**: {name}\n**When**: {asctime}\n"
                      "     **In**: {filename}:{funcName}:{lineno}\n"
                      "         ```{message}```",
            'style': '{'
        },
        'file_formatter': {
            'format': "%(asctime)s:%(level_initial)s:%(name)s:\n"
                      "       in %(filename)s:%(funcName)s:%(lineno)s:\n"
                      "               %(message)s",
            #'style': '{'
        },
        'stdout_formatter': {
            'format': "%(asctime)s:%(log_color)s%(levelname)s%(reset)s:%(name_log_color)s%(name)s%(reset)s:\n"
                      "       in %(file_log_color)s%(filename)s:%(funcName)s:%(lineno)s%(reset)s\n"
                      "               %(message_log_color)s%(message)s%(reset)s",
            '()': 'colorlog.ColoredFormatter',
            'secondary_log_colors': secondary_log_colors,
            'reset': True,
            'log_colors': log_colors,
        }
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'file_formatter',
            'filename': 'discord.log',
            'filters': ['level_filter'],
            'mode': 'w+'
        },
        'stream_handler': {
            '()': 'colorlog.StreamHandler',
            'formatter': 'stdout_formatter',
            # 'filters': ['level_filter'],

        },
        'discord_handler': {
            'sender_name': f'AgeBot',
            'avatar_url': "https://images-ext-2.discordapp.net/external/bYpfdlmDpj9gJZ6R7TjNKmbpfEWlhVXfkVj81dCo-30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/929996821571452969/1ceae3ca5833bd12ee758c6e62cbf45f.png?width=468&height=468",
            '()': DiscordHandler,
            'formatter': 'discord_format',
            'regular_message_text': '',
            'embeds_title': f'Log Message from ',
            'filters': ['emoji_filter', 'escape_markdown'],
            'webhook_url': Configs.hook.outgoing.nenrei_dev,

        },
        'telegram_handler': {
            '()': TelegramHandler,
            'token': Configs.hook.telegram.token,
            'channel_id': Configs.hook.telegram.chat_id,
            'formatter': 'telegram_formatter',
            'parse_mode': Configs.hook.telegram.parse_mode
        }
    },
    # 'loggers': {
    #     'discord': {
    #         'handlers': handlers,
    #         'filters': ['emoji_filter']
    #     },
    #     'gateway': {
    #         'handlers': handlers,
    #         'propagate': False
    #     },
    #     'discord.client': {
    #         'handlers': handlers,
    #         'propagate': False,
    #         'filters': ['emoji_filter']
    #     }
    # },
    'root': {
        'handlers': handlers,
        'level': 'NOTSET'
    },
})


logger = logging
