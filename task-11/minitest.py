import os
import importlib
import argparse
from multiprocessing import Pool
from runner import run_single_test


def discover_tests(test_dir):
    tests = []

    for file in os.listdir(test_dir):
        if file.startswith("test_") and file.endswith(".py"):
            module_name = file[:-3]
            module = importlib.import_module(f"{test_dir}.{module_name}")

            for attr in dir(module):
                obj = getattr(module, attr)

                if callable(obj) and hasattr(obj, "_is_test"):
                    if hasattr(obj, "_params"):
                        for param in obj._params:
                            tests.append((obj, param))
                    else:
                        tests.append((obj, None))

    return tests


def run_all_tests(tests, workers, verbose):
    if workers > 1:
        with Pool(workers) as p:
            results = p.starmap(run_single_test,
                                [(t, p, verbose) for t, p in tests])
    else:
        results = [run_single_test(t, p, verbose) for t, p in tests]

    return results


def print_results(results, verbose):
    passed = failed = skipped = 0
    total_time = 0

    for status, name, msg, duration in results:
        total_time += duration

        if status == "PASS":
            passed += 1
        elif status == "FAIL":
            failed += 1
        elif status == "SKIP":
            skipped += 1

        if verbose or status != "PASS":
            print(f"{status:5} {name} [{duration:.2f}s]")
            if msg:
                print(f"   → {msg}")

    print("\n=== Summary ===")
    print(f"{len(results)} tests | {passed} passed | {failed} failed | {skipped} skipped")
    print(f"Total time: {total_time:.2f}s")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("path")
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    if args.command != "run":
        print("Unknown command")
        return

    print("=== Test Discovery ===")
    tests = discover_tests(args.path)
    print(f"Found {len(tests)} tests")

    print(f"\n=== Execution ({args.parallel} workers) ===")
    results = run_all_tests(tests, args.parallel, args.verbose)

    print_results(results, args.verbose)


if __name__ == "__main__":
    main()