PLUGIN_REGISTRY = {}

def register_plugin(cls):
    PLUGIN_REGISTRY[cls.name] = cls
    return cls