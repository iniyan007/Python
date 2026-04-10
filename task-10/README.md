# 📘 **Blockchain Prototype**

---

# 🔷 1. Overview

This project implements a **simplified blockchain system** in Python that simulates core concepts of modern decentralized systems like Bitcoin.

The system includes:

* Proof-of-Work mining
* Digital transaction signing (ECDSA)
* Peer-to-peer communication using sockets
* Block propagation across nodes
* Wallet and balance tracking

Each node runs independently and maintains its own blockchain while communicating with peers.

---

# 🎯 2. Objectives

* Understand blockchain fundamentals
* Implement decentralized node communication
* Simulate mining and consensus basics
* Demonstrate secure transactions using cryptography

---

# ⚙️ 3. Technologies Used

* **Python**
* `hashlib` → SHA-256 hashing
* `ecdsa` → Digital signatures
* `socket` → Peer-to-peer networking
* `threading` → Concurrent node handling
* JSON → Data serialization

---

# 🧱 4. System Architecture

```txt
Wallet → Transaction → Mempool → Mining → Block → Broadcast → Chain
```

---

## 🔹 Components

### 1. Wallet

* Generates private/public key pair
* Creates unique address
* Signs transactions

### 2. Transaction

* Contains sender, receiver, amount
* Digitally signed for authenticity
* Verified using public key

### 3. Block

* Contains transactions
* Includes:

  * Previous hash
  * Merkle root
  * Nonce
  * Timestamp

### 4. Blockchain

* Linked list of blocks
* Maintains:

  * Chain
  * Mempool
  * Mining difficulty

### 5. Node

* Runs server
* Connects to peers
* Broadcasts blocks
* Handles incoming data

---

# 🔐 5. Cryptography

Transactions are secured using **Elliptic Curve Digital Signature Algorithm (ECDSA)**:

* Private key → signs transaction
* Public key → verifies signature

```python
vk.verify(signature, message)
```

Ensures:

* Authenticity
* Integrity
* Non-repudiation

---

# 🌳 6. Merkle Tree

Transactions inside a block are hashed into a **Merkle Root**.

### Process:

* Hash each transaction
* Pair hashes and hash again
* Repeat until one hash remains

This ensures:

* Efficient verification
* Data integrity

---

# ⛏️ 7. Proof of Work

Mining involves finding a nonce such that:

```txt
hash starts with "0000"
```

### Algorithm:

```python
while not hash.startswith("0000"):
    nonce += 1
```

---

## Purpose:

* Prevent spam
* Secure the network
* Introduce computational cost

---

# 🌐 8. Peer-to-Peer Networking

Nodes communicate using **TCP sockets**.

### Features:

* Each node listens on a port
* Connects to peers manually
* Broadcasts mined blocks

```python
self.broadcast({
    "type": "BLOCK",
    ...
})
```

---

# 🔄 9. Block Propagation

When a block is mined:

1. Broadcast to peers
2. Peers receive block
3. Validate:

   * Transactions
   * Previous hash
4. Append to chain

---

# 💸 10. Transaction Flow

1. User creates transaction
2. Transaction is signed
3. Added to mempool
4. Included in mined block
5. Block is broadcast

---

# 💰 11. Balance Calculation

Balances are **not stored**.

Instead:

```python
for block in chain:
    for tx in block.transactions:
        update balance
```

---

# 🧪 12. Execution Flow

### Step 1: Start Nodes

```bash
python node.py 5001
python node.py 5002
python node.py 5003
```

---

### Step 2: Create Transaction

```txt
Node-1 → Send coins to Node-2
```

---

### Step 3: Mine Block

```txt
Node mines block → includes transaction + reward
```

---

### Step 4: Broadcast

```txt
Block sent to all peers
```

---

### Step 5: Validation

```txt
Nodes verify and append block
```

---

### Step 6: Check Balance

```txt
Balances updated based on chain
```

---

# 📊 13. Sample Output

```txt
[NODE-5002] Received block #2
[NODE-5002] Block accepted!

Balance: 2.0
```

---

# 🧠 16. Key Learnings

* Blockchain is a **distributed ledger**, not a database
* Security comes from:

  * Cryptography
  * Hashing
  * Consensus
* Nodes must **independently verify data**
* Balance is derived from **history**, not stored

---

# 📌 17. Conclusion

This project successfully demonstrates:

* Core blockchain mechanics
* Distributed node communication
* Secure transaction handling
* Proof-of-work mining

It serves as a strong foundation for understanding real-world systems like Ethereum.
