from core.plugin_base import PluginBase
from core.registry import register_plugin

@register_plugin
class ImageOptimizer(PluginBase):
    name = "image-optimizer"
    version = "0.9.1"

    def activate(self, context):
        context["post_processors"].append("image-opt")
        print("— registered: post-processor for .png/.jpg")