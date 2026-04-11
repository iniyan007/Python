import json
import os

WAL_FILE = "graph.wal"

class WAL:
    def log(self, entry):
        with open(WAL_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def recover(self, storage):
        if not os.path.exists(WAL_FILE):
            return

        with open(WAL_FILE, "r") as f:
            for line in f:
                entry = json.loads(line.strip())

                if entry["type"] == "CREATE_NODE":
                    storage.create_node(entry["label"], entry["props"], entry["id"])

                elif entry["type"] == "CREATE_EDGE":
                    storage.create_edge(entry["from"], entry["to"], entry["etype"], entry["props"])