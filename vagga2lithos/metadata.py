import yaml

try:
    from yaml import CSafeDumper as BaseDumper
except ImportError:
    from yaml import SafeDumper as BaseDumper


class Dumper(BaseDumper):
    pass


def header(info):
    header = "# v2l: # This file is generated by vagga2lithos\n"
    header += ''.join("# v2l: " + line
        for line in yaml.dump(info, Dumper=Dumper).splitlines(True))
    return header
