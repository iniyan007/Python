fixtures = {}

def fixture(scope="function"):
    def decorator(func):
        fixtures[func.__name__] = {
            "func": func,
            "scope": scope
        }
        return func
    return decorator


def resolve_fixtures(test_func):
    import inspect

    params = inspect.signature(test_func).parameters
    resolved = {}

    for name in params:
        if name in fixtures:
            f = fixtures[name]["func"]
            gen = f()

            if hasattr(gen, "__next__"):
                value = next(gen)
                resolved[name] = value
            else:
                resolved[name] = gen

    return resolved