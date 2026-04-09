import importlib
import os
from core.registry import PLUGIN_REGISTRY

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.context = {
            "commands": {},
            "themes": {},
            "processors": [],
            "post_processors": []
        }

    def discover_plugins(self, plugin_dir="plugins"):
        print(f"[CORE] Scanning plugin directory: ./{plugin_dir}/")

        discovered = []

        for folder in os.listdir(plugin_dir):
            try:
                module = importlib.import_module(f"{plugin_dir}.{folder}.plugin")
                discovered.append(folder)
            except Exception as e:
                print(f"Failed loading {folder}: {e}")

        print(f"[CORE] Discovered {len(discovered)} plugins:")
        for name, cls in PLUGIN_REGISTRY.items():
            deps = f"(depends: {', '.join(cls.dependencies)})" if cls.dependencies else ""
            print(f"├── {cls.name} v{cls.version} ({cls.plugin_type} {deps})")

    def load_plugins(self):
        for name, cls in PLUGIN_REGISTRY.items():
            self.plugins[name] = cls()

    def resolve_dependencies(self):
        print("\n[CORE] Resolving dependencies...")

        visited = []
        resolved = []

        def visit(plugin):
            if plugin.name in visited:
                return
            visited.append(plugin.name)

            for dep in plugin.dependencies:
                visit(self.plugins[dep])

            resolved.append(plugin)

        for plugin in self.plugins.values():
            visit(plugin)

        for p in resolved:
            if p.dependencies:
                print(f"{p.name} -> {', '.join(p.dependencies)} OK (satisfied)")
            else:
                print(f"{p.name} (no dependencies) OK")

        return resolved

    def activate_plugins(self, ordered_plugins):
        print("\n[CORE] Activating plugins in order...")

        for i, plugin in enumerate(ordered_plugins, start=1):
            plugin.activate(self.context)
            print(f"[{i}/{len(ordered_plugins)}] {plugin.name}.activate()")