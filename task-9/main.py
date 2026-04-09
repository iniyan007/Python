from core.plugin_manager import PluginManager

def main():
    print("=== Application Startup ===")
    print("$ sitegen build --theme dark-mode\n")

    manager = PluginManager()

    manager.discover_plugins()
    manager.load_plugins()

    ordered = manager.resolve_dependencies()
    manager.activate_plugins(ordered)

if __name__ == "__main__":
    main()