def print_match_results(results):
    print("+----------+-----------+")
    print("| p.name   | c.name    |")
    print("+----------+-----------+")

    for r in results:
        print(f"| {r[0].get('name','')} | {r[1].get('name','')} |")

    print("+----------+-----------+")
    print(f"{len(results)} row(s) returned")


def print_path(storage, path):
    names = [
        storage.nodes[n]["props"].get("name", str(n))
        for n in path
    ]
    print("Path:", " -> ".join(names))
    print(f"Length: {len(path)-1} hops")