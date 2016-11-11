import yaml

try:
    from yaml import CSafeDumper as BaseDumper
except ImportError:
    from yaml import SafeDumper as BaseDumper


class Dumper(BaseDumper):

    def statedir_repr(self, value):
        return self.represent_mapping('!Statedir', value.__dict__)

    def toplevel_repr(self, value):
        return self.represent_mapping('tag:yaml.org,2002:map',
            value.format(), flow_style=False)

    def list_repr(self, value):
        return self.represent_sequence('tag:yaml.org,2002:seq',
            value, flow_style=False)

    def quoted_repr(self, value):
        return self.represent_scalar('tag:yaml.org,2002:str',
            str(value), style='"')


class Statedir(object):
    pass


# Formatting
class List(list): pass
class Quoted(str): pass


class Toplevel(dict):

    def format(self):
        x = self.copy()
        yield 'kind', x.pop('kind')
        yield 'user-id', x.pop('user-id')
        yield 'group-id', x.pop('group-id')
        yield 'environ', x.pop('environ')
        yield 'memory-limit', x.pop('memory-limit')
        yield 'fileno-limit', x.pop('fileno-limit')
        yield 'cpu-shares', x.pop('cpu-shares')
        yield 'executable', x.pop('executable')
        yield 'arguments', List(map(Quoted, x.pop('arguments')))
        for k, v in x.items():
            yield k, v


yaml.add_representer(Statedir, Dumper.statedir_repr, Dumper=Dumper)
yaml.add_representer(Toplevel, Dumper.toplevel_repr, Dumper=Dumper)
yaml.add_representer(List, Dumper.list_repr, Dumper=Dumper)
yaml.add_representer(Quoted, Dumper.quoted_repr, Dumper=Dumper)


def dump(data, file):
    yaml.dump(Toplevel(data), file, Dumper=Dumper)
