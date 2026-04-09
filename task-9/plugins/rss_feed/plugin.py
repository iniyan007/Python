from core.plugin_base import PluginBase
from core.registry import register_plugin

@register_plugin
class RSSFeed(PluginBase):
    name = "rss-feed"
    version = "1.0.0"
    dependencies = ["markdown-parser"]

    def activate(self, context):
        context["commands"]["generate-rss"] = True
        print('— registered: command "generate-rss"')