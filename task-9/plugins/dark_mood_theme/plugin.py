from core.plugin_base import PluginBase
from core.registry import register_plugin

@register_plugin
class DarkModeTheme(PluginBase):
    name = "dark-mode-theme"
    version = "1.3.2"

    def activate(self, context):
        context["themes"]["dark-mode"] = "enabled"
        print('— registered: theme "dark-mode"')