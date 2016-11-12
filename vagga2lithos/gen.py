import click

from . import vagga
from . import lithos
from .main import main as cli
from .human import panic


@cli.command()
@click.option('-f', '--input', default='vagga.yaml',
    help='The vagga.yaml file to read')
@click.argument('vagga-command', default='run')
def generate(input, vagga_command):
    data = vagga.load_yaml(input)
    cmd = data['commands'].get(vagga_command)
    if cmd is None:
        panic("Command {} not found", vagga_command)

    output = _convert_cmd(cmd)

    import sys
    lithos.dump(output, sys.stdout)


def _convert_cmd(cmd):
    run = cmd.run
    if isinstance(run, list):
        run = run
    else:
        run = ['sh', '-ec', run]
    return {
        'kind': 'Daemon',
        'user-id': 1,
        'group-id': 1,
        'environ': {
            # TODO(tailhook) gather from vagga.yaml
        },
        # TODO(tailhook) workdir
        # TODO(tailhook) search path in PATH and in container
        'executable': run[0],
        'arguments': run[1:],
        'memory-limit': '1Ti', # TODO(tailhook) basically no limit so far
        'fileno-limit': 65536, # Should be fine, docker uses it by default
        'cpu-shares': 1024,
        'volumes': {
            '/state': lithos.Statedir(),
        },
    }
