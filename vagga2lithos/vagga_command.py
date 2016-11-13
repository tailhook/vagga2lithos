DEFAULT_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


def extract_command_info(vagga, cmd):
    container = vagga['containers'][cmd.container]

    env = container.get('environ', {}).copy()
    env.update(getattr(cmd, 'environ', {}))

    cli = cmd.run
    if isinstance(cli, str):
        cli = ['/bin/sh', '-ec', cli]

    if not cli[0].startswith('/'):
        path = filter(bool, env.get('PATH', DEFAULT_PATH).split(':'))
        raise NotImplementedError(
            "Search in {!r} is not implemented yet".format(path))


    return {
        'environ': env,
        'executable': cli[0],
        'arguments': cli[1:],
    }
