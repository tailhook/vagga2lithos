import sys
import copy
import difflib

import click

from . import vagga
from . import lithos
from . import metadata
from .main import main as cli
from .human import panic
from .vagga_command import extract_command_info



def careful_update(old_config, old_info, new_info, *, verbose):
    new_config = copy.deepcopy(old_config)

    if old_info['executable'] != new_info['executable']:
        if verbose:
            print("Executable changed {} -> {}".format(
                old_info['executable'], new_info['executable']))
        if old_config['executable'] == old_info['executable']:
            new_config['executable'] = new_info['executable']
        else:
            if verbose:
                print("Skipping executable change because it was overriden")

    if old_info['arguments'] != new_info['arguments']:
        if verbose:
            print("Arguments changed {!r} -> {!r}".format(
                old_info['arguments'], new_info['arguments']))
        if (old_config['executable'] == old_info['executable'] and
                old_config['arguments'] == old_info['arguments']):
            new_config['arguments'] = new_info['arguments']
        else:
            if verbose:
                print("Skipping arguments change because they were overriden")
            print(old_config['executable'] , old_info['executable'],
                old_config['arguments'] , old_info['arguments'])

    if old_info['environ'] != new_info['environ']:
        old_cfg = old_config['environ']
        old_env = old_info['environ']
        new_env = new_info['environ']
        old_set = set(old_env)
        new_set = set(new_env)

        for key in old_set - new_set:
            if verbose: print("Removed env var {!r}".format(key))
            new_config['environ'].pop(key)

        for key in old_set & new_set:
            if (old_cfg.get(key) == old_env[key] and
                    old_env[key] != new_env[key]):
                if verbose: print("Update env var {!r}".format(key))
                new_config['environ'][key] = new_env[key]
            else:
                if verbose: print("Skipping updated env var {!r}".format(key))

        for key in new_set - old_set:
            new_config['environ'][key] = new_env[key]

    return new_config



@cli.command()
@click.option('-f', '--input', default='vagga.yaml',
    help='The vagga.yaml file to read')
@click.option('-l', '--lithos-file', default='lithos.yaml',
    help='The lithos.yaml file to read')
@click.option('-v', '--verbose/--quiet', default=False,
    help='Print diagnostic messsages')
@click.argument('vagga-command', default='run')
def check(input, vagga_command, lithos_file, verbose):
    data = vagga.load_yaml(input)
    cmd = data['commands'].get(vagga_command)
    if cmd is None:
        panic("Command {!r} not found", vagga_command)
    if cmd.__class__.__name__ == 'Command':

        info = extract_command_info(data, cmd)
        header = metadata.read_header(lithos_file)
        if info == header:
            if verbose:
                print("Everything is up to date")
            sys.exit(0)
        else:
            if verbose:
                print("Changes needed")
                old_config = lithos.read(lithos_file)
                new_config = careful_update(old_config, header, info,
                    verbose=verbose)
                old = lithos.dump(old_config)
                new = lithos.dump(new_config)
                print("Proposed changes:", lithos_file)
                print('\n'.join(difflib.ndiff(old.splitlines(),
                                            new.splitlines())))
            sys.exit(1)

    else:
        raise NotImplementedError(cmd)