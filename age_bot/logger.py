import colorlog

from asyncio.subprocess import STDOUT
import sys
import discord


class LevelFilter(colorlog.Filter):
    """
    This is a filter which changes the levelname to that of its Initial letter

    """

    def filter(self, record):
        record.levelname = record.levelname[0]
        return True


logger = colorlog.getLogger('discord')
logger.setLevel(colorlog.INFO)
handler = colorlog.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
handler2 = colorlog.StreamHandler(sys.stdout)
handler.setFormatter(colorlog.ColoredFormatter("%(asctime)s:%(levelname)s:%(name)s:\n"
                                               "       in %(filename)s:%(funcName)s:%(lineno)s\n"
                                               "               %(message)s",
                                               reset=True,
                                               log_colors={
                                                   'DEBUG': 'cyan',
                                                   'INFO': 'green',
                                                   'WARNING': 'yellow',
                                                   'ERROR': 'red',
                                                   'CRITICAL': 'red,bg_white',
                                               },
                                               secondary_log_colors={},
                                               ))
handler2.setFormatter(colorlog.ColoredFormatter("%(asctime)s:%(levelname)s:%(name)s:\n"
                                                "       in %(filename)s:%(funcName)s:%(lineno)s\n"
                                                "               %(message)s",
                                                reset=True,
                                                log_colors={
                                                    'DEBUG': 'cyan',
                                                    'INFO': 'green',
                                                    'WARNING': 'yellow',
                                                    'ERROR': 'red',
                                                    'CRITICAL': 'red,bg_white',
                                                },
                                                secondary_log_colors={},
                                                ))
logger.addHandler(handler)
logger.addHandler(handler2)
f = LevelFilter()
logger.addFilter(f)
