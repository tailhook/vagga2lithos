import yaml

try:
    from yaml import CSafeDumper as BaseDumper
    from yaml import CSafeLoader as BaseLoader
except ImportError:
    from yaml import SafeDumper as BaseDumper
    from yaml import SafeLoader as BaseLoader


class Loader(BaseLoader):

    def container_load(self, node):
        return Container(self.construct_scalar(node))

    def ensure_dir_load(self, node):
        return EnsureDir(self.construct_scalar(node))

    def include_load(self, node):
        return Include(self.construct_scalar(node))

    def unpack_load(self, node):
        return Unpack(self.construct_sequence(node))

    def copy_load(self, node):
        return Copy(**self.construct_mapping(node))


class Dumper(BaseDumper):

    def container_repr(self, value):
        return self.represent_scalar("!Container", value.name, style='"')

    def ensure_dir_repr(self, value):
        return self.represent_scalar("!EnsureDir", value.dir, style='"')

    def include_repr(self, value):
        return self.represent_scalar("!*Include", value.file, style='"')

    def unpack_repr(self, value):
        return self.represent_sequence("!*Unpack", value.items,
            flow_style=True)

    def copy_repr(self, value):
        return self.represent_mapping("!Copy", value.__dict__)

    def generic_object_repr(self, value):
        return self.represent_mapping("!"+value.__class__.__name__,
            value.__dict__)

    def generic_list_repr(self, value):
        return self.represent_sequence("!"+value.__class__.__name__, value)

    def generic_str_repr(self, value):
        return self.represent_scalar("!"+value.__class__.__name__, value)


class Container(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


class EnsureDir(object):

    def __init__(self, dir):
        self.dir = dir

    def __eq__(self, other):
        return self.dir == other.dir


class Include(object):

    def __init__(self, file):
        self.file = file

    def __eq__(self, other):
        return self.file == other.file

class Unpack(object):

    def __init__(self, items):
        self.items = items

    def __eq__(self, other):
        return self.items == other.items


class Copy(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        return type(self) == type(other) and self.__dict__ == other.__dict__



def unknown_type(loader, tag, node):
    if isinstance(node, yaml.MappingNode):
        typ = type(tag, (object,), {
            '__init__': lambda self, **kwargs: self.__dict__.update(kwargs),
            '__eq__': lambda self, other: self.__dict__ == other.__dict__,
        })
        yaml.add_representer(typ, Dumper.generic_object_repr, Dumper=Dumper)
        return typ(**loader.construct_mapping(node))
    elif isinstance(node, yaml.SequenceNode):
        typ = type(tag, (list,), {})
        yaml.add_representer(typ, Dumper.generic_list_repr, Dumper=Dumper)
        return typ(loader.construct_sequence(node))
    elif isinstance(node, yaml.ScalarNode):
        typ = type(tag, (str,), {})
        yaml.add_representer(typ, Dumper.generic_str_repr, Dumper=Dumper)
        return typ(loader.construct_scalar(node))
    else:
        raise NotImplementedError(node)


yaml.add_constructor("!EnsureDir", Loader.ensure_dir_load, Loader=Loader)
yaml.add_representer(EnsureDir, Dumper.ensure_dir_repr, Dumper=Dumper)
yaml.add_constructor("!Container", Loader.container_load, Loader=Loader)
yaml.add_representer(Container, Dumper.container_repr, Dumper=Dumper)
yaml.add_constructor("!Copy", Loader.copy_load, Loader=Loader)
yaml.add_representer(Copy, Dumper.copy_repr, Dumper=Dumper)

yaml.add_constructor("!*Include", Loader.include_load, Loader=Loader)
yaml.add_representer(Include, Dumper.include_repr, Dumper=Dumper)
yaml.add_constructor("!*Unpack", Loader.unpack_load, Loader=Loader)
yaml.add_representer(Unpack, Dumper.unpack_repr, Dumper=Dumper)

yaml.add_multi_constructor("!", unknown_type, Loader=Loader)


class Config(object):
    def __init__(self, containers, commands):
        self.containers = containers
        self.commands = commands

    @classmethod
    def load(Config, path):
        with open(str(path)) as f:
            return Config(**yaml.load(f, Loader=Loader))


def dump(data, file=None):
    return yaml.dump(data, file, Dumper=Dumper,
        default_flow_style=False, default_style='')

def load_partial(path):
    with open(str(path)) as f:
        return yaml.load(f, Loader=Loader)
