import sys


def panic(pattern, *args, **kwargs):
    print(pattern.format(*args, **kwargs), file=sys.stderr)
    sys.stderr.flush()
    sys.exit(1)
