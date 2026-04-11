class QueryEngine:
    def __init__(self, storage):
        self.storage = storage

    def match(self, label1, edge1, edge2, label2, where_key=None, where_val=None):
        results = []

        for nid, node in self.storage.nodes.items():
            if node["label"] != label1:
                continue

            for e1 in self.storage.edges[nid]:
                if e1["type"] != edge1:
                    continue

                mid = e1["to"]

                for e2 in self.storage.edges[mid]:
                    if e2["type"] != edge2:
                        continue

                    end = e2["to"]
                    end_node = self.storage.nodes[end]

                    if end_node["label"] != label2:
                        continue

                    if where_key:
                        if end_node["props"].get(where_key) != where_val:
                            continue

                    results.append((node["props"], end_node["props"]))

        return results