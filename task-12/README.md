# 📘 Graph Database Engine (Python)

## 🧠 Overview

This project is a **custom in-memory graph database engine** inspired by systems like Neo4j graph database.
It supports:

* Node and edge creation
* Multi-hop traversal queries
* Shortest path computation
* Indexing for fast lookup
* Write-Ahead Logging (WAL) for persistence
* Interactive CLI shell

---

# ⚙️ System Architecture

```
User Input (CLI)
       ↓
main.py (Command Parser)
       ↓
graphdb.py (Core Controller)
       ↓
---------------------------------
| Storage | Query | Traversal | WAL |
---------------------------------
       ↓
Output (Formatted Results)
```

---

# 📂 Module Breakdown

---

## 🔹 1. `main.py` (CLI Interface)

### Responsibility:

* Accepts user commands
* Parses input
* Calls appropriate database functions

### Example Flow:

```bash
CREATE NODE alice Person name=Alice
```

➡️ Parsed and passed to:

```python
db.create_node(name, label, props)
```

---

## 🔹 2. `graphdb.py` (Core Engine)

### Role:

Acts as the **central controller** connecting all modules.

### Components:

* `Storage` → Data storage
* `WAL` → Persistence
* `Traversal` → Graph algorithms
* `QueryEngine` → Query execution

### Example:

```python
def create_node(self, name, label, props):
    nid = self.storage.create_node(label, props)
    self.wal.log(...)
```

👉 Handles:

* Business logic
* Logging
* Mapping names → IDs

---

## 🔹 3. `storage.py` (Data Layer)

### Data Structures:

#### Nodes:

```python
{
  1: { "label": "Person", "props": {"name": "Alice"} }
}
```

#### Edges (Adjacency List):

```python
{
  1: [{ "to": 2, "type": "FRIENDS_WITH" }]
}
```

---

### 📌 Why Adjacency List?

* Efficient traversal
* O(1) neighbor access
* Memory efficient

---

### Indexing:

```python
{
  "Person.name": {
    "Alice": [1]
  }
}
```

👉 Enables faster filtering instead of scanning all nodes

---

## 🔹 4. `wal.py` (Write-Ahead Logging)

### Purpose:

Ensures **data durability**

---

### Logging Example:

```json
{"type": "CREATE_NODE", "id": 1, "label": "Person", "props": {"name": "Alice"}}
```

---

### Recovery Process:

On restart:

```python
wal.recover(storage)
```

👉 Replays all operations to rebuild state

---

### 🔥 Key Concept:

Even if memory is lost → WAL restores everything

---

## 🔹 5. `query.py` (Query Engine)

### Function:

Executes **pattern-based graph queries**

---

### Query Logic:

```python
Person --FRIENDS_WITH--> X --WORKS_AT--> Company
```

---

### Execution Steps:

1. Filter nodes by label
2. Traverse first edge
3. Traverse second edge
4. Apply condition (WHERE)
5. Return matching results

---

### Example Output:

```
Alice → Acme
```

---

## 🔹 6. `traversal.py` (Graph Algorithms)

### Algorithm Used: BFS (Breadth-First Search)

---

### Why BFS?

* Guarantees shortest path in unweighted graph
* Efficient for traversal queries

---

### Logic:

1. Start from source node
2. Explore neighbors level-by-level
3. Stop when target found

---

### Shortest Path Principle:

\text{Shortest Path} = \text{Minimum number of edges between nodes}

---

### Example:

```
Alice → Bob → Acme
Length = 2 hops
```

---

## 🔹 7. `utils.py` (Helpers)

### Functions:

* Format table output
* Print traversal path

---

# 🔄 Execution Flow Example

## Command:

```bash
CREATE EDGE bob WORKS_AT acme
```

### Step-by-step:

1. CLI reads command
2. `main.py` parses input
3. Calls:

   ```python
   db.create_edge("bob", "acme")
   ```
4. `graphdb.py`:

   * Converts names → IDs
   * Stores edge in memory
   * Logs operation in WAL
5. Output printed

---

# 📊 Sample Output

```
=== Graph DB Shell ===

CREATE NODE alice Person name=Alice age=30
CREATE NODE bob Person name=Bob age=28
CREATE NODE acme Company name=Acme

CREATE EDGE alice FRIENDS_WITH bob
CREATE EDGE bob WORKS_AT acme

MATCH
→ Alice | Acme

SHORTEST_PATH alice acme
→ Alice → Bob → Acme

STATS
→ Nodes: 3 | Edges: 2
→ WAL size: 429 bytes
```

---

# 🚀 Features Implemented

✔ In-memory graph storage
✔ Typed nodes and edges
✔ Multi-hop traversal queries
✔ Shortest path (BFS)
✔ Hash-based indexing
✔ Write-Ahead Logging (WAL)
✔ Crash recovery
✔ CLI-based query interface

---

# 🧠 Key Concepts Demonstrated

* Graph Data Structures
* BFS Traversal
* Hash Indexing
* Database Internals (WAL)
* Query Execution Engine
* Modular System Design

---

# 🏁 Conclusion

This project simulates core components of a real-world graph database like Neo4j graph database, showcasing strong understanding of:

* Data structures
* Algorithms
* Backend system design
* Database internals
