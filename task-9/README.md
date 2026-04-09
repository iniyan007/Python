# 📦 Plugin Architecture with Dynamic Module Loading

## 📌 Overview

This system implements a **modular plugin architecture** in Python that allows dynamic discovery, loading, and execution of plugins at runtime.

The core application remains unchanged while plugins extend functionality such as:

* Themes
* Content processors
* Post-processors
* CLI commands (extendable)

---

## 🧱 Architecture Components

### 1. **Core Application (`main`)**

The entry point responsible for:

* Initializing the plugin manager
* Discovering plugins
* Loading and resolving dependencies
* Activating plugins in correct order

```python
def main():
    manager = PluginManager()
    manager.discover_plugins()
    manager.load_plugins()
    ordered = manager.resolve_dependencies()
    manager.activate_plugins(ordered)
```

---

### 2. **Plugin Base Class (`PluginBase`)**

Defines a standard interface for all plugins.

#### Key Features:

* Enforces structure using `ABC`
* Supports lifecycle hooks
* Allows dependency declaration

```python
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
```

---

### 3. **Plugin Registry (`PLUGIN_REGISTRY`)**

A global registry where plugins are automatically registered using a decorator.

```python
PLUGIN_REGISTRY = {}

def register_plugin(cls):
    PLUGIN_REGISTRY[cls.name] = cls
    return cls
```

#### Benefits:

* Decouples plugin discovery from instantiation
* Enables dynamic loading
* Simplifies plugin management

---

### 4. **Plugin Manager (`PluginManager`)**

Central controller responsible for plugin lifecycle.

#### Responsibilities:

* Discover plugins
* Load plugin instances
* Resolve dependencies
* Activate plugins

---

## 🔍 Plugin Lifecycle

### Step 1: Discovery

Scans the `./plugins/` directory and dynamically imports modules.

```python
importlib.import_module(f"{plugin_dir}.{folder}.plugin")
```

✔ Automatically triggers registration via decorator

---

### Step 2: Loading

Creates instances of all registered plugins.

```python
self.plugins[name] = cls()
```

---

### Step 3: Dependency Resolution

Resolves plugin execution order using a **Depth-First Search (DFS)** approach (topological sort).

```python
def visit(plugin):
    for dep in plugin.dependencies:
        visit(self.plugins[dep])
```

✔ Ensures:

* Dependencies load before dependents
* No manual ordering required

---

### Step 4: Activation

Executes plugins in dependency-safe order.

```python
plugin.activate(self.context)
```

---

## 🧠 Shared Context System

Plugins interact via a shared `context` dictionary:

```python
self.context = {
    "commands": {},
    "themes": {},
    "processors": [],
    "post_processors": []
}
```

### Example:

* Theme plugin → updates `themes`
* Parser plugin → adds to `processors`
* Optimizer → adds to `post_processors`

---

## 🔌 Example Plugins

### 1. Dark Mode Theme

```python
class DarkModeTheme(PluginBase):
    name = "dark-mode-theme"

    def activate(self, context):
        context["themes"]["dark-mode"] = "enabled"
```

✔ Adds UI theme support

---

### 2. Markdown Parser

```python
class MarkdownParser(PluginBase):
    name = "markdown-parser"
    plugin_type = "built-in"

    def activate(self, context):
        context["processors"].append("md->html")
```
✔ Converts `.md` → HTML
---

### 3. Image Optimizer

```python
class ImageOptimizer(PluginBase):
    name = "image-optimizer"

    def activate(self, context):
        context["post_processors"].append("image-opt")
```

✔ Optimizes images after processing

---

## 🔗 Dependency Management

Plugins declare dependencies:

```python
dependencies = ["markdown-parser"]
```

✔ Guarantees:

* Correct load order
* No missing dependency execution

---

## ⚙️ Key Features

### ✅ Dynamic Module Loading

* Uses `importlib`
* No hardcoded imports

### ✅ Extensibility

* Add/remove plugins without modifying core

### ✅ Dependency Resolution

* Automatic ordering using graph traversal

### ✅ Lifecycle Hooks

* `activate()` and optional `deactivate()`

### ✅ Decoupled Design

* Plugins interact only via shared context

---

## ⚠️ Error Handling

Current system:

```python
except Exception as e:
    print(f"Failed loading {folder}: {e}")
```

### Recommended Improvements:

* Log errors instead of printing
* Skip faulty plugins gracefully
* Detect circular dependencies

---

## 🚀 Future Enhancements

### 1. Entry Points (`pyproject.toml`)

Allow plugins to be installed via pip:

```toml
[project.entry-points."myapp.plugins"]
dark = "dark_mode.plugin:DarkModeTheme"
```

---

### 2. Sandboxed Execution

* Run plugins in isolated environments
* Prevent unsafe operations

---

### 3. CLI Command Plugins

Extend:

```python
context["commands"]
```

---

### 4. Version Compatibility Checks

Ensure:

* Plugin version compatibility
* Dependency version constraints

---

### 5. Circular Dependency Detection

Add cycle detection in DFS

---

## 📊 Execution Flow Summary

```
START
  ↓
Scan plugins directory
  ↓
Import modules (auto-register)
  ↓
Instantiate plugins
  ↓
Resolve dependencies (topological sort)
  ↓
Activate plugins in order
  ↓
Application ready
```

---

## 🧩 Use Case

This architecture is ideal for:

* Static site generators (like your `$ sitegen build`)
* Developer tools
* CLI frameworks
* CMS systems
* IoT dashboards (your domain 👀)

---

## 🏁 Conclusion

This plugin system provides:

* High modularity
* Scalability
* Clean separation of concerns

It closely resembles real-world systems like:

* VS Code extensions
* Webpack plugins
* Django apps
