# built-in
import os
import sys
import logging

# 3rd party
import colorlog
from logging_disgram.logging_handlers import DiscordHandler, TelegramHandler

# local
from age_bot.config import Configs
from age_bot.logger.dicts import log_colors, secondary_log_colors
from age_bot.logger.filters import emoji_filter, level_filter, escape_markdown

logger = logging.getLogger('discord')
logger.setLevel(colorlog.DEBUG)


async def init_loggers():
    """Initialize the loggers"""
    ################
    #  Formatters  #
    ################
    discord_format = logging.Formatter(
        "{level_emoji}->**{levelname}** \n**Logger**: {name}\n**When**: {asctime}\n"
        "     **In**: {filename}:{funcName}:{lineno}\n"
        "         ```{message}```", style='{')
    telegram_format = logging.Formatter(
        "<b>%(levelname)s</b> <b>%(name)s</b> <b>%(asctime)s</b>\n"
        "     <b>%(filename)s</b> <b>%(funcName)s</b> <b>%(lineno)s</b>\n"
        "         ```%(message)s```", )
    file_format = logging.Formatter(
        "%(asctime)s:%(level_initial)s:%(name)s:\n"
        "       in %(filename)s:%(funcName)s:%(lineno)s:\n"
        "               %(message)s", )

    stdout_format = colorlog.ColoredFormatter(
        "%(asctime)s:%(log_color)s%(levelname)s%(reset)s:%(name_log_color)s%(name)s%(reset)s:\n"
        "       in %(file_log_color)s%(filename)s:%(funcName)s:%(lineno)s%(reset)s\n"
        "               %(message_log_color)s%(message)s%(reset)s",
        secondary_log_colors=secondary_log_colors,
        reset=True,
        log_colors=log_colors)
    ####################################
    #             Handlers             #
    #  Add formatters to handlers too  #
    ####################################

    file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
    file_handler.setFormatter(file_format)
    stream_handler = colorlog.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(stdout_format)
    discord_handler = DiscordHandler(formatter=discord_format,
                                     sender_name=f"AgeBot {' beta' if os.environ['AGEBOT_ENV'] == 'dev' else ''}",
                                     avatar_url="https://images-ext-2.discordapp.net/external/bYpfdlmDpj9gJZ6R7TjNKmbpfEWlhVXfkVj81dCo-30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/929996821571452969/1ceae3ca5833bd12ee758c6e62cbf45f.png?width=468&height=468",
                                     regular_message_text='',
                                     embeds_title=f"Log Message from '{'DevBot' if os.environ['AGEBOT_ENV'] == 'dev' else ''}'",
                                     webhook_url=Configs.hook.outgoing.nenrei_dev
                                     )
    telegram_handler = TelegramHandler(formatter=telegram_format,
                                       token=Configs.hook.telegram.token,
                                       channel_id=Configs.hook.telegram.chat_id,
                                       parse_mode=Configs.hook.telegram.parse_mode)

    #############################
    #  Add Filters to Handlers  #
    #############################
    discord_handler.addFilter(escape_markdown)
    discord_handler.addFilter(emoji_filter)
    stream_handler.addFilter(level_filter)
    telegram_handler.addFilter(escape_markdown)
    telegram_handler.addFilter(emoji_filter)
    for handler in [discord_handler, stream_handler, file_handler, telegram_handler]:
        logger.addHandler(handler)
