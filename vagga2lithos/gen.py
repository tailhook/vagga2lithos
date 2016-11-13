import click

from . import vagga
from . import lithos
from . import metadata
from .main import main as cli
from .human import panic
from .vagga_command import extract_command_info


@cli.command()
@click.option('-f', '--input', default='vagga.yaml',
    help='The vagga.yaml file to read')
@click.argument('vagga-command', default='run')
def generate(input, vagga_command):
    data = vagga.load_yaml(input)
    cmd = data['commands'].get(vagga_command)
    if cmd is None:
        panic("Command {!r} not found", vagga_command)
    if cmd.__class__.__name__ == 'Command':
        info = extract_command_info(data, cmd)
        output = _convert_cmd(info)
        header = metadata.header(info)
        text = header + lithos.dump(output)
        print(text)
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
