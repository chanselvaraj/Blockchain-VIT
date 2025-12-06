import hashlib
import json
import time
import uuid

# ------------------------
# Wallet and UTXO system
# ------------------------

class Wallet:
    def __init__(self, name=None):
        self.name = name or str(uuid.uuid4())[:8]
        self.address = str(uuid.uuid4().hex[:16])  # unique address

    def to_dict(self):
        return {"name": self.name, "address": self.address}


class TxInput:
    def __init__(self, txid, index):
        self.txid = txid
        self.index = index

    def to_dict(self):
        return {"txid": self.txid, "index": self.index}


class TxOutput:
    def __init__(self, amount, address):
        self.amount = amount
        self.address = address

    def to_dict(self):
        return {"amount": self.amount, "address": self.address}


class Transaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.txid = str(uuid.uuid4().hex)

    def to_dict(self):
        return {
            "txid": self.txid,
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [o.to_dict() for o in self.outputs]
        }


# ------------------------
# Block and Blockchain
# ------------------------

class Block:
    def __init__(self, index, previous_hash, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = int(time.time())
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "transactions": [tx.to_dict() for tx in self.transactions]
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [tx.to_dict() for tx in self.transactions]
        }


class Blockchain:
    def __init__(self, difficulty=4, coinbase_amount=1, genesis_amount=100):
        self.chain = []
        self.mempool = []
        self.wallets = {}  # name -> Wallet
        self.utxos = {}  # address -> list of outputs
        self.difficulty = difficulty
        self.coinbase_amount = coinbase_amount

        # Create genesis block
        self.genesis_amount = genesis_amount
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_wallet = Wallet("genesis")
        self.wallets[genesis_wallet.name] = genesis_wallet
        coinbase_tx = Transaction([], [TxOutput(self.genesis_amount, genesis_wallet.address)])
        block = Block(0, "0"*64, [coinbase_tx], nonce=0)
        self.chain.append(block)
        self.add_utxos(coinbase_tx)

    # ------------------------
    # Wallet management
    # ------------------------
    def create_wallet(self, name):
        if name in self.wallets:
            return self.wallets[name].to_dict()
        w = Wallet(name)
        self.wallets[name] = w
        self.utxos[w.address] = []
        return w.to_dict()

    def get_balance(self, address):
        return sum([o["amount"] for o in self.utxos.get(address, [])])

    # ------------------------
    # Transaction management
    # ------------------------
    def create_transaction(self, sender_addr, receiver_addr, amount):
        if self.get_balance(sender_addr) < amount:
            raise Exception("Insufficient funds")
        # Select UTXOs
        spent = []
        accumulated = 0
        for utxo in list(self.utxos[sender_addr]):
            spent.append(utxo)
            accumulated += utxo["amount"]
            if accumulated >= amount:
                break
        # Remove spent UTXOs
        for utxo in spent:
            self.utxos[sender_addr].remove(utxo)
        # Create outputs
        outputs = [TxOutput(amount, receiver_addr)]
        change = accumulated - amount
        if change > 0:
            outputs.append(TxOutput(change, sender_addr))
        tx = Transaction([TxInput(u["txid"], u["index"]) for u in spent], outputs)
        self.mempool.append(tx)
        return tx.to_dict()

    def add_utxos(self, tx):
        for idx, o in enumerate(tx.outputs):
            self.utxos.setdefault(o.address, []).append({
                "amount": o.amount,
                "txid": tx.txid,
                "index": idx
            })

    # ------------------------
    # Mining
    # ------------------------
    def mine_block(self, miner_address=None):
        # Include coinbase transaction first
        coinbase_tx = Transaction([], [TxOutput(self.coinbase_amount, miner_address)]) if miner_address else None
        txs = [coinbase_tx] + self.mempool if coinbase_tx else self.mempool.copy()
        index = len(self.chain)
        previous_hash = self.chain[-1].hash
        nonce = 0

        while True:
            block = Block(index, previous_hash, txs, nonce)
            if block.hash.startswith("0"*self.difficulty):
                break
            nonce += 1

        # Add block
        self.chain.append(block)
        # Update UTXO
        for tx in txs:
            self.add_utxos(tx)
        self.mempool.clear()
        return block.to_dict()

    # ------------------------
    # Utilities
    # ------------------------
    def to_dict(self):
        return {
            "chain": [b.to_dict() for b in self.chain],
            "mempool": [tx.to_dict() for tx in self.mempool],
            "wallets": {k: w.address for k, w in self.wallets.items()},
            "utxos": self.utxos
        }
