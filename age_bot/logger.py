import colorlog
import logging
from asyncio.subprocess import STDOUT
import sys
import discord


class LevelFilter(logging.Filter):
    """
    This is a filter which changes the levelname to that of its Initial letter

    """

    def filter(self, record):
        record.levelname = record.levelname[0]
        return True
secondary_log_colors = {
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
}
logger = colorlog.getLogger('discord')
logger.setLevel(colorlog.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
handler2 = colorlog.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s:\n"
        "       in %(filename)s:%(funcName)s:%(lineno)s:\n"
        "               %(message)s"
    ))
handler2.setFormatter(
    colorlog.ColoredFormatter(
        "%(asctime)s:%(log_color)s%(levelname)s%(reset)s:%(name_log_color)s%(name)s%(reset)s:\n"
        "       in %(file_log_color)s%(filename)s:%(funcName)s:%(lineno)s%(reset)s\n"
        "               %(message_log_color)s%(message)s%(reset)s",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
            'D': 'cyan',
            'I': 'green',
            'W': 'yellow',
            'E': 'red',
            'C': 'red,bg_white',
        },
        secondary_log_colors=secondary_log_colors,
    ))
logger.addHandler(handler)
logger.addHandler(handler2)
f = LevelFilter()
logger.addFilter(f)
