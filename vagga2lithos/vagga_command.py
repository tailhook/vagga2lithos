import os.path


DEFAULT_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


def extract_command_info(vagga, cmd, *, workdir_base):
    container = vagga.containers[cmd.container]

    env = container.get('environ', {}).copy()
    env.update(getattr(cmd, 'environ', {}))
    env.setdefault('PATH', DEFAULT_PATH)

    cli = cmd.run
    if isinstance(cli, str):
        cli = ['/bin/sh', '-ec', cli]

    if not cli[0].startswith('/'):
        path = filter(bool, env.get('PATH', DEFAULT_PATH).split(':'))
        raise NotImplementedError(
            "Search in {!r} is not implemented yet".format(path))

    workdir = getattr(cmd, 'work-dir', '/work')
    if workdir == '/work':
        workdir = workdir_base
    elif workdir.startswith('/work/'):
        workdir = workdir_base + workdir[len('/work'):]
    else:
        workdir = os.path.join(workdir_base, workdir)

    return {
        'environ': env,
        'executable': cli[0],
        'arguments': cli[1:],
        'work-dir': workdir,
    }
