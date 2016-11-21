import os
import click

from . import lithos
from . import metadata
from .main import main as cli
from .human import panic
from .vagga_command import extract_command_info
from .vagga import Config as Vagga


@cli.command()
@click.option('-f', '--input', default='vagga.yaml',
    help='The vagga.yaml file to read')
@click.argument('vagga-command', default='run')
@click.argument('output', default='-')
def generate(input, vagga_command, output=None):
    vagga = Vagga.load(input)
    cmd = vagga.commands.get(vagga_command)
    if cmd is None:
        panic("Command {!r} not found", vagga_command)
    text = generate_command(vagga, cmd)
    if output and output != '-':
        with open(output + '.tmp', 'wt') as f:
            f.write(text)
        os.rename(output + '.tmp', output)
    else:
        print(text)

def generate_command(vagga, cmd):
    if cmd.__class__.__name__ == 'Command':
        info = extract_command_info(vagga, cmd)
        output = _convert_cmd(info)
        header = metadata.dump_header(info)
        return header + lithos.dump(output)
    else:
        raise NotImplementedError(cmd)


def _convert_cmd(info):
    return {
        'kind': 'Daemon',
        'user-id': 1,
        'group-id': 1,
        'environ': info['environ'],
        # TODO(tailhook) workdir
        'executable': info['executable'],
        'arguments': info['arguments'],
        'memory-limit': '1Ti', # TODO(tailhook) basically no limit so far
        'fileno-limit': 65536, # Should be fine, docker uses it by default
        'cpu-shares': 1024,
        'volumes': {
            '/state': lithos.Statedir(),
        },
    }
