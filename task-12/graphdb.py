from storage import Storage
from wal import WAL
from traversal import Traversal
from query import QueryEngine

import os

class GraphDB:
    def __init__(self):
        self.storage = Storage()
        self.wal = WAL()
        self.traversal = Traversal(self.storage)
        self.query_engine = QueryEngine(self.storage)

        self.name_to_id = {}

        self.wal.recover(self.storage)

    def create_node(self, name, label, props):
        nid = self.storage.create_node(label, props)
        self.name_to_id[name] = nid

        self.wal.log({
            "type": "CREATE_NODE",
            "id": nid,
            "label": label,
            "props": props
        })

        print(f"Node created: {label}#{nid}")

    def create_edge(self, from_name, to_name, etype):
        from_id = self.name_to_id[from_name]
        to_id = self.name_to_id[to_name]

        self.storage.create_edge(from_id, to_id, etype, {})

        self.wal.log({
            "type": "CREATE_EDGE",
            "from": from_id,
            "to": to_id,
            "etype": etype,
            "props": {}
        })

        print(f"Edge created: {from_name} —{etype}-> {to_name}")

    def match(self):
        results = self.query_engine.match(
            "Person", "FRIENDS_WITH", "WORKS_AT", "Company", "name", "Acme"
        )
        return results

    def shortest_path(self, start, end):
        return self.traversal.shortest_path(
            self.name_to_id[start],
            self.name_to_id[end]
        )

    def stats(self):
        nodes = len(self.storage.nodes)
        edges = sum(len(v) for v in self.storage.edges.values())
        wal_size = os.path.getsize("graph.wal") if os.path.exists("graph.wal") else 0

        print(f"Nodes: {nodes} | Edges: {edges}")
        print(f"Indexes: {len(self.storage.index)}")
        print(f"WAL size: {wal_size} bytes")