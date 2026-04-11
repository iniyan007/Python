from collections import defaultdict

class Storage:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)
        self.index = defaultdict(lambda: defaultdict(list))
        self.node_id = 0

    def create_node(self, label, props, nid=None):
        if nid is None:
            self.node_id += 1
            nid = self.node_id
        else:
            self.node_id = max(self.node_id, nid)

        self.nodes[nid] = {"label": label, "props": props}

        for k, v in props.items():
            self.index[f"{label}.{k}"][v].append(nid)

        return nid

    def create_edge(self, from_id, to_id, etype, props):
        self.edges[from_id].append({
            "to": to_id,
            "type": etype,
            "props": props
        })