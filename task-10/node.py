from email.mime import message
import hashlib
import json
import socket
import threading
import time
from ecdsa import SigningKey, VerifyingKey, SECP256k1

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def address(self):
        return sha256(self.public_key.to_string().hex())[:16]

    def sign(self, message):
        return self.private_key.sign(message.encode()).hex()

    def get_public_key(self):
        return self.public_key.to_string().hex()

class Transaction:
    def __init__(self, sender, receiver, amount, signature="", pub_key=""):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
        self.pub_key = pub_key

    def to_dict(self):
        return self.__dict__

    def hash(self):
        return sha256(json.dumps({
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }, sort_keys=True))

    def sign_transaction(self, wallet):
        self.pub_key = wallet.get_public_key()
        self.signature = wallet.sign(self.hash())

    def is_valid(self):
        if self.sender == "SYSTEM":
            return True
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(self.pub_key), curve=SECP256k1)
            vk.verify(bytes.fromhex(self.signature), self.hash().encode())
            return True
        except:
            return False

def merkle_root(transactions):
    hashes = [tx.hash() for tx in transactions]

    if not hashes:
        return ""

    while len(hashes) > 1:
        temp = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                temp.append(sha256(hashes[i] + hashes[i + 1]))
            else:
                temp.append(hashes[i])
        hashes = temp
    return hashes[0]

class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.timestamp = time.time()
        self.merkle_root = merkle_root(transactions)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.prev_hash}{self.timestamp}{self.nonce}{self.merkle_root}"
        return sha256(data)

    def mine(self, difficulty):
        prefix = "0" * difficulty
        print(f"[MINING] Block #{self.index}...")

        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"[SUCCESS] Block mined: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis()]
        self.difficulty = 4
        self.mempool = []

    def create_genesis(self):
        genesis = Block(0, [], "0")
        genesis.timestamp = 1234567890
        genesis.nonce = 0
        genesis.hash = genesis.calculate_hash()
        
        return genesis

    def add_transaction(self, tx):
        if not tx.is_valid():
            return

        if tx.sender != "SYSTEM":
            if self.get_balance(tx.sender) < tx.amount:
                print("[ERROR] Insufficient balance!")
                return

        self.mempool.append(tx)

    def mine_block(self, miner_address):
        reward_tx = Transaction("SYSTEM", miner_address, 1.0)
        self.mempool.append(reward_tx)

        block = Block(len(self.chain), self.mempool, self.chain[-1].hash)
        block.mine(self.difficulty)

        self.chain.append(block)
        self.mempool = []

        return block

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        return balance


class Node:
    def __init__(self, port):
        self.port = port
        self.peers = []
        self.blockchain = Blockchain()
        self.wallet = Wallet()

        print(f"[NODE] Running on port {self.port} | Wallet: {self.wallet.address()}")

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", self.port))
        server.listen()

        while True:
            client, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        try:
            data = client.recv(4096).decode()
            message = json.loads(data)

            if message["type"] != "BLOCK":
                client.close()
                return

            data = message["data"]
            print(f"[NODE-{self.port}] Received block #{data['index']}")

            transactions = []
            for tx_data in data["transactions"]:
                tx = Transaction(**tx_data)
                transactions.append(tx)
            block = Block(
                data["index"],
                transactions,
                data["prev_hash"]
            )

            block.hash = data["hash"]
            block.nonce = data["nonce"]
            for tx in block.transactions:
                if not tx.is_valid():
                    print(f"[NODE-{self.port}] Invalid transaction detected!")
                    client.close()
                    return
            if block.prev_hash == self.blockchain.chain[-1].hash:
                self.blockchain.chain.append(block)
                print(f"[NODE-{self.port}] Block accepted!")
            else:
                print(f"[NODE-{self.port}] Block rejected!")

        except Exception as e:
            print(f"[ERROR] {e}")

        finally:
            client.close()

    def connect_peer(self, port):
        self.peers.append(("localhost", port))

    def broadcast(self, message):
        for peer in self.peers:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(peer)
                s.send(json.dumps(message).encode())
                s.close()
            except:
                pass

    def create_transaction(self, to, amount):
        tx = Transaction(self.wallet.address(), to, amount)
        tx.sign_transaction(self.wallet)

        print(f"[TX] {self.wallet.address()} -> {to} : {amount}")
        self.blockchain.add_transaction(tx)

    def mine(self):
        block = self.blockchain.mine_block(self.wallet.address())
        self.broadcast({
            "type": "BLOCK",
            "data": {
                "index": block.index,
                "prev_hash": block.prev_hash,
                "hash": block.hash,
                "nonce": block.nonce,
                "transactions": [tx.to_dict() for tx in block.transactions]
            }
        })

    def balance(self):
        return self.blockchain.get_balance(self.wallet.address())


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1])
    node = Node(port)

    if port == 5001:
        node.connect_peer(5002)
        node.connect_peer(5003)
    elif port == 5002:
        node.connect_peer(5001)
        node.connect_peer(5003)
    elif port == 5003:
        node.connect_peer(5001)
        node.connect_peer(5002)

    threading.Thread(target=node.start_server, daemon=True).start()

    time.sleep(2)

    while True:
        print("\n1. Send Transaction\n2. Mine Block\n3. Balance\n")
        choice = input("Choose: ")

        if choice == "1":
            to = input("Receiver: ")
            amt = float(input("Amount: "))
            node.create_transaction(to, amt)

        elif choice == "2":
            node.mine()

        elif choice == "3":
            print("Balance:", node.balance())