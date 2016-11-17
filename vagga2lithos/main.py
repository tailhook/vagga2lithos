import click


@click.group()
def main():
    pass

# load commands
from . import gen, update
