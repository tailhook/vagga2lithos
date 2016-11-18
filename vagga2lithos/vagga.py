import yaml

try:
    from yaml import CSafeLoader as BaseLoader
except ImportError:
    from yaml import SafeLoader as BaseLoader


class Loader(BaseLoader):
    pass


def unknown_type(loader, tag, node):
    if isinstance(node, yaml.MappingNode):
        typ = type(tag, (object,), {
            '__init__': lambda self, **kwargs: self.__dict__.update(kwargs)
        })
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


class Config(object):
    def __init__(self, containers, commands):
        self.containers = containers
        self.commands = commands

    @classmethod
    def load(Config, path):
        with open(path) as f:
            return Config(**yaml.load(f, Loader=Loader))
