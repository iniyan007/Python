from collections import deque

class Traversal:
    def __init__(self, storage):
        self.storage = storage

    def shortest_path(self, start, end):
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            node, path = queue.popleft()

            if node == end:
                return path

            visited.add(node)

            for edge in self.storage.edges[node]:
                if edge["to"] not in visited:
                    queue.append((edge["to"], path + [edge["to"]]))

        return None