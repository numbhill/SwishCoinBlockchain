import hashlib
import json
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash="0")  # ✅ Ensure method accepts this

    def create_block(self, transactions=None, previous_hash="0"):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(time.time()),
            "transactions": transactions or [],
            "previous_hash": previous_hash,
        }

        block["hash"] = self.hash(block)  # Hash the block
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_last_block(self):
        return self.chain[-1] if self.chain else None
