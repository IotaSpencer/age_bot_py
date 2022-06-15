import logging
from asyncio.subprocess import STDOUT
import sys
import discord
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
handler2 = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname[0])s:%(name):"
                                       "       in %(filename)s:%(funcName)s:%(lineno)s"
                                       "               %(message)s"))
handler2.setFormatter(logging.Formatter("%(asctime)s:%(levelname[0])s:%(name)s:"
                                        "       in %(filename)s:%(funcName)s:%(lineno)s"
                                        "               %(message)s"))
logger.addHandler(handler)
logger.addHandler(handler2)
