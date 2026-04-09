from abc import ABC, abstractmethod

class PluginBase(ABC):
    name = ""
    version = ""
    dependencies = []
    plugin_type = "third-party"

    @abstractmethod
    def activate(self, context):
        pass

    def deactivate(self, context):
        pass