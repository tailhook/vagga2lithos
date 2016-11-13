import yaml

try:
    from yaml import CSafeDumper as BaseDumper
    from yaml import CSafeLoader as BaseLoader
except ImportError:
    from yaml import SafeDumper as BaseDumper
    from yaml import SafeLoader as BaseLoader


class Dumper(BaseDumper):

    def statedir_repr(self, value):
        return self.represent_mapping('!Statedir', value.__dict__)

    def toplevel_repr(self, value):
        return self.represent_mapping('tag:yaml.org,2002:map',
            value.format(), flow_style=False)

    def list_repr(self, value):
        return self.represent_sequence('tag:yaml.org,2002:seq',
            value, flow_style=False)

    def map_repr(self, value):
        return self.represent_mapping('tag:yaml.org,2002:map',
            sorted((k, Quoted(v)) for k, v in value.items()),
            flow_style=False)

    def tag_map_repr(self, value):
        return self.represent_mapping('!' + value.__class__.__name__,
            value.__dict__)

    def quoted_repr(self, value):
        return self.represent_scalar('tag:yaml.org,2002:str',
            str(value), style='"')

class Loader(BaseLoader):
    pass


class Statedir(object):
    pass


# Formatting
class List(list): pass
class Map(dict): pass
class Quoted(str): pass


class Toplevel(dict):

    def format(self):
        x = self.copy()
        yield 'kind', x.pop('kind')
        yield 'user-id', x.pop('user-id')
        yield 'group-id', x.pop('group-id')
        yield 'environ', Map(x.pop('environ'))
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
yaml.add_representer(Map, Dumper.map_repr, Dumper=Dumper)
yaml.add_representer(Quoted, Dumper.quoted_repr, Dumper=Dumper)

def unknown_type(loader, tag, node):
    if isinstance(node, yaml.MappingNode):
        typ = type(tag, (object,), {
            '__init__': lambda self, **kwargs: self.__dict__.update(kwargs)
        })
        yaml.add_representer(typ, Dumper.tag_map_repr, Dumper=Dumper)
        return typ(**loader.construct_mapping(node))
    elif isinstance(node, yaml.SequenceNode):
        typ = type(tag, (list,), {})
        return typ(loader.construct_sequence(node))
    elif isinstance(node, yaml.ScalarNode):
        typ = type(tag, (str,), {})
        return typ(loader.construct_scalar(node))
    else:
        raise NotImplementedError(node)


yaml.add_multi_constructor("!", unknown_type, Loader=Loader)

def dump(data, *args, **kwargs):
    return yaml.dump(Toplevel(data), *args, Dumper=Dumper, **kwargs)

def read(filename):
    with open(filename) as f:
        return yaml.load(f, Loader=Loader)
