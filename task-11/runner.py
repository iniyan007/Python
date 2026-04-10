import time
import traceback
from fixtures import resolve_fixtures


def run_single_test(test_func, param=None, verbose=False):
    name = test_func.__name__

    if param:
        name += f"[{param}]"

    if hasattr(test_func, "_skip"):
        return ("SKIP", name, test_func._skip_reason, 0)

    start = time.time()

    try:
        kwargs = resolve_fixtures(test_func)

        if param:
            kwargs.update(param)

        test_func(**kwargs)

        duration = time.time() - start
        return ("PASS", name, "", duration)

    except AssertionError as e:
        duration = time.time() - start
        return ("FAIL", name, str(e), duration)

    except Exception:
        duration = time.time() - start
        return ("ERROR", name, traceback.format_exc(), duration)