import logging, datetime, sys, json_logging, flask, colorlog, discord
from asyncio.subprocess import STDOUT
from custom_handlers.logging_handlers import DiscordHandler, TelegramHandler
import logging.config
from age_bot.config import Configs
from logging import LogRecord

class LevelFilter(logging.Filter):
    """
    This is a filter which changes the levelname to that of its Initial letter

    """

    def filter(self, record):
        record.levelname = record.levelname[0]
        return True

class EmojiFilter(logging.Filter):
    """This is a filter that replaces levelname with emojis"""
    def filter(self, record: LogRecord) -> bool:
        level = record.levelname
        levels = {
            'WARNING': '⚠',
            'ERROR': '‼',
            'CRITICAL': '☠',
            'DEBUG': '❓',
            'INFO': '✔'
        }
        try:
            record.level_emoji = levels[level]
            return True
        except:
            return False
telegram_chat_id = Configs.hook.telegram.chat_ids[0] # type: list
logging.config.dictConfig({
    'version': 1,
    'filters': {
        'level_filter': {
            '()': LevelFilter,
        },
        'emoji_filter': {
            '()': EmojiFilter,

        }
    },
    'formatters': {
        'telegram_formatter': {
            'format': "<b>%(levelname)s</b> <b>%(name)s</b> <b>%(asctime)s</b>\n"
                      "     <b>%(filename)s</b> <b>%(funcName)s</b> <b>%(lineno)s</b>"
                      "         ```%(message)s```"
        },
        'file_formatter': {
            'format':   "%(asctime)s:%(levelname)s:%(name)s:\n"
                        "       in %(filename)s:%(funcName)s:%(lineno)s:\n"
                        "               %(message)s"
        },
        'stdout_formatter': {
            'format':   "%(asctime)s:%(log_color)s%(levelname)s%(reset)s:%(name_log_color)s%(name)s%(reset)s:\n"
                        "       in %(file_log_color)s%(filename)s:%(funcName)s:%(lineno)s%(reset)s\n"
                        "               %(message_log_color)s%(message)s%(reset)s",
       		'()': 'colorlog.ColoredFormatter',
            'secondary_log_colors': {
                'message': {
                    'E': 'red',
                    'C': 'red',
                    'W': 'yellow',
                    'I': 'green',
                    'D': 'blue',
                },
                'traceback': {
                    'E': 'red',
                    'C': 'red',
                    'W': 'yellow',
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
            },
            'reset': True,
            'log_colors': {
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
        }
    },
    'handlers': {
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file_formatter',
            'filename': 'discord.log',
            'mode': 'w+'
        },
        'stream_handler': {
            'level': 'INFO',
            'class': 'colorlog.StreamHandler',
            'formatter': 'stdout_formatter',
            'filters': ['level_filter']

        },
        'discord_handler': {
            'sender_name': 'AgeBot',
            'regular_message_text': '',
            'embeds_title': 'Log Message',
            'webhook_url': Configs.hook.outgoing.nenrei_dev,

        },
        'telegram_handler': {
            'token': Configs.hook.telegram.token,
            'channel_id': telegram_chat_id,
            'formatter': 'telegram_formatter',
            'parse_mode': Configs.hook.telegram.parse_mode
        }
    },
    'loggers': {
        'discord': {
            'handlers': ['telegram_handler', 'file_handler', 'stream_handler', 'discord_handler']
        }
    },

})

logger = logging
