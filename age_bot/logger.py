import logging
from asyncio.subprocess import STDOUT
import sys
import discord
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
handler2 = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(f"{asctime}:{levelname[0]}:{name}:"
                                       f"       in {filename}:{funcName}:{lineno!s}"
                                       f"               {message}"))
handler2.setFormatter(logging.Formatter(f"{asctime}:{levelname[0]}:{name}:"
                                        f"       in {filename}:{funcName}:{lineno}"
                                        f"               {message}"))
logger.addHandler(handler)
logger.addHandler(handler2)
