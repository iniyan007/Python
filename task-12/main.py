from graphdb import GraphDB
from utils import print_match_results, print_path

def main():
    db = GraphDB()

    print("=== Graph DB Shell ===")

    while True:
        cmd = input("graphdb> ").strip()

        if cmd.startswith("CREATE NODE"):
            parts = cmd.split()
            name = parts[2]
            label = parts[3]

            props = {}
            for p in parts[4:]:
                k, v = p.split("=")
                props[k] = v

            db.create_node(name, label, props)

        elif cmd.startswith("CREATE EDGE"):
            parts = cmd.split()
            db.create_edge(parts[2], parts[4], parts[3])

        elif cmd.startswith("MATCH"):
            results = db.match()
            print_match_results(results)

        elif cmd.startswith("SHORTEST_PATH"):
            parts = cmd.split()
            path = db.shortest_path(parts[1], parts[2])

            if path:
                print_path(db.storage, path)
            else:
                print("No path found")

        elif cmd.startswith("STATS"):
            db.stats()

        elif cmd == "exit":
            break

        else:
            print("Unknown command")

if __name__ == "__main__":
    main()