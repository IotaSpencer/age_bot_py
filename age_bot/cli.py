import os.path
import os
import asyncclick as click
import age_bot.bot.client
from collections.abc import MutableMapping
from multiprocessing import Process,Queue,Pipe

class AgeBotCLI(MutableMapping):
    def __init__(self, home=None, debug=False):
        self.home = home
        self.debug = debug
        home = os.path.expanduser('~') or home

    def __setitem__(self, k, v):
        setattr(self, k, v)
    def __getitem__(self, k):
        getattr(self, k)
    def __delitem__(self, k):
        self[k] = None
    def __iter__(self):
        raise NotImplementedError
    def __len__(self):
        raise NotImplementedError



@click.group()
@click.option('--debug/--no-debug', default=False, envvar='AGEBOT_DEBUG')
@click.option('--env', '-e', default='prod', envvar='AGEBOT_ENV',
              type=click.Choice(['prod', 'dev'], case_sensitive=False))
@click.pass_context
def cli(ctx, debug, env):
    ctx.obj = AgeBotCLI(debug)
    ctx.obj.env = env
    os.environ['AGEBOT_ENV'] = env


@cli.command()
@click.pass_context
async def start(ctx):
    await age_bot.bot.client.start(ctx.obj.env)
    from age_bot.logger import logger, init_loggers
    init_loggers()


@cli.command()
async def repl():
    import code
    code.interact(local=globals())


@cli.command
async def deploy_commands():
    pass
