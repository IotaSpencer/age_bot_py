import os.path
import asyncclick as click
import age_bot.bot.client


class AgeBotCLI(object):
    def __init__(self, home=None, debug=False):
        self.debug = debug
        home = os.path.expanduser('~') or home


@click.group()
@click.option('--debug/--no-debug', default=False, envvar='AGEBOT_DEBUG')
@click.pass_context
def cli(ctx, debug):
    ctx.obj = AgeBotCLI(debug)


@cli.command()
async def start():
    await age_bot.bot.client.start()


@cli.command()
async def repl():
    import code
    code.interact(local=globals())


@cli.command
async def deploy_commands():
    pass
