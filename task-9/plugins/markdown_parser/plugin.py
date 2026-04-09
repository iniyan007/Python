from core.plugin_base import PluginBase
from core.registry import register_plugin

@register_plugin
class MarkdownParser(PluginBase):
    name = "markdown-parser"
    version = "2.1.0"
    plugin_type = "built-in"

    def activate(self, context):
        context["processors"].append("md->html")
        print("— registered: .md -> HTML converter")