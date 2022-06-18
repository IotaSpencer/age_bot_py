# built-in
from typing import Union, List, Optional

# 3rd-party
import discord
from discord import Guild, Member, User, TextChannel, Message, Bot
from discord.ext.bridge import BridgeApplicationContext, BridgeExtContext
from discord.ext.commands import Context
from discord.commands import ApplicationContext
from omegaconf.dictconfig import DictConfig

# local
from age_bot.config import Configs


def check_if_tester_or_main_bot(ctx: Union[Context, Message, Member, ApplicationContext], bot: Bot) -> bool:
    if ctx.__class__.__name__ in ['Message']:
        message = ctx # type: Union[Message, BridgeExtContext]
        if bot.user.id == 719736166819037314 or (message.author.id in Configs.devconfig.bot.testers or message.author.id in Configs.config.bot.testers):
            return True
        else:
            return False
    elif ctx.__class__.__name__ in ['Member']:
        member = ctx # type: Member
        if bot.user.id == 719736166819037314 or (member.id in Configs.devconfig.bot.testers or member.id in Configs.config.bot.testers):
            return True
        else:
            return False
    else:
        ctx = ctx # type: Union[Context, ApplicationContext]
        if bot.user.id == 719736166819037314 or (ctx.user.id in Configs.devconfig.bot.testers or ctx.user.id in Configs.config.bot.testers):
            return True
        else:
            return False

async def reply_self_is_dev(ctx: Union[Context, Message, Member, ApplicationContext]):
    nenrei_user = ctx.bot.get_user(719736166819037314)
    member = ctx.user if ctx.user else ctx.author
    self_is_dev_string = f"""
    Hello {member_distinct(member)},
    This is the development(alpha/beta) bot for {user_distinct(nenrei_user)}
    
    You should see if there is another command that has "{nenrei_user.name}" next to it.
    Instead of "{ctx.bot.user.name}"
    """
    if ctx.__class__.__name__ == 'Context' or ctx.__class__.__name__ == 'Message':
        await ctx.reply(self_is_dev_string)
    elif ctx.__class__.__name__ == 'ApplicationContext':
        await ctx.respond(content=self_is_dev_string)

async def reply_self_is_dev2(message: Message, bot: Bot):
    nenrei_user = bot.get_user(719736166819037314) # type: User
    member = message.author # type: User
    self_is_dev_string = f"""
    Hello {member_distinct(member)},
    This is the development(alpha/beta) bot for {user_distinct(nenrei_user)}
    
    You should probably be sending this to Nenrei-Sama.
    
    Depending on what you're sending, Here's your options.
    
        * If you're saying 'Hi' or something like that, then you're dumb,
            as this is not a chat bot.
            
        * If you are trying to verify your ID+tag, then you need to run the '/verify'
            command that has '{nenrei_user.name}' next to it, not 'DevBot for Nenrei-Sama'
        
        * If you're asking a question about verification, ask in #hello on the server that
            you have in common with me, if there are multiple, then ask in the one you're trying 
            to currently verify in.
        
        * If you're interested in Nenrei-Sama/DevBot for Nenrei-Sama, please speak to/message
            our owner {bot.get_user(bot.owner_id)}
            
        *** Anything else that hasn't been anticipated, most likely is nonsense."""
    await message.reply(self_is_dev_string)

def member_distinct(member: discord.Member) -> str:
    """
    From a discord.Member object return the member's username and discrim
    as username#0000

    :param member: a discord member object
    :return: str
    """
    return "{}#{}".format(member.name, member.discriminator)


author_distinct = member_distinct
user_distinct = member_distinct


def is_not_adult(member: Member, guild: Guild):
    """
    :rtype: bool
    :arg member: Guild Member
    :arg guild: Guild
    """
    try:
        adult_role = guild.get_role(Configs.serverdb.servers[str(guild.id)].role)
        member_roles = member.roles
        if not member.bot:
            member_is_not_adult = adult_role not in member_roles
            return member_is_not_adult
        else:
            return False
    except ConfigKeyError:
        raise GuildNotInDBError


def grab_guild(ctx: ApplicationContext):
    if ctx.guild:
        return ctx.guild
    else:
        raise NoGuildInContextError


def find_shamed(channels: List[TextChannel]) -> TextChannel:
    for channel in channels:
        if channel.name == 'named-and-shamed':
            return channel  # type: TextChannel
    return None


def is_slash_command(ctx: Union[BridgeApplicationContext, BridgeExtContext]):
    if ctx.__class__.__name__ == BridgeApplicationContext:
        return True
    else:
        return False


def has_role(user, role):
    if role in user.roles:
        return True
    else:
        return False


def server_confirm_roles(server: Guild, way: Optional[str]) -> List[discord.Role] | List[str] | List[DictConfig]:
    """
    :param way: how to return the roles
    :param server: Guild to check confirm'able roles on
    :return: list[discord.Role]
    """
    # usually just admin and mod roles
    server_id = server.id
    guild_db_obj = Configs.serverdb.servers[str(server_id)]
    roles = guild_db_obj.can_confirm
    server_roles = server.roles
    confirm_roles = [role for role in server_roles if role.id in roles]
    if way == 'list-of-name':  # returns List[str]
        return [role.name for role in confirm_roles]
    elif way == 'list-of-role':  # returns List[discord.Role]
        return [role for role in confirm_roles]
    else:
        return roles  # otherwise, do whatever we want with the object and return DictConfig


def has_server_confirm_role(server: Guild, user: Union[Member, User]) -> bool:
    """
    Check if 'user' has 'confirmable' role in 'server'

    :param server: Guild to check against
    :param user: user to check roles of
    :return: bool
    """
    s_c_rs = server_confirm_roles(server, 'list-of-role')
    shared_roles = []
    for role in s_c_rs:
        if has_role(user, role):
            shared_roles.append(role)
    if shared_roles:
        return True
    else:
        return False


def server_helper_roles(server: Guild, way: Optional[str]) -> List[discord.Role] | List[str] | List[DictConfig]:
    """
    Get a list of 'helper' roles in 'server' and return them in a certain 'way'

    :param way: how to return roles
    :param server: Guild to check helper roles on
    :return: Union[List[str], List[discord.Role], DictConfig]
    """
    # usually just 'Server Helpers'
    server_id = server.id
    guild_db_obj = Configs.serverdb.servers[str(server_id)]
    roles = guild_db_obj.can_help
    server_roles = server.roles
    help_roles = [role for role in server_roles if role.id in roles]
    if way == 'list-of-name':  # returns List[str]
        return [role.name for role in help_roles]
    elif way == 'list-of-role':  # returns List[discord.Role]
        return [role for role in help_roles]
    else:
        return roles  # otherwise do whatever we want with the object


def has_server_helper_role(server: Guild, user: Union[Member, User]) -> bool:
    """

    :param server: Guild to check
    :param user: User to check
    :return: bool
    """
    s_c_rs = server_helper_roles(server, 'list-of-role')
    shared_roles = []
    for role in s_c_rs:
        if has_role(user, role):
            shared_roles.append(role)
    if shared_roles:
        return True
    else:
        return False


async def get_adult_role(ctx):
    return ctx.guild.get_role(Configs.serverdb.servers[str(ctx.guild.id)].role)
