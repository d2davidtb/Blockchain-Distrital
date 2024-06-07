import json
from typing import List
from uuid import UUID

from core.helpers import custom_hash_md5
from core.models.merkle_tree import MerkleTree
from core.models.coinbase import Coinbase
from core.models.transaction import Transaction

class Block:
    id: int
    merkle_tree: MerkleTree
    transactions: List[Transaction]
    nonce: int
    previous_hash: str
    current_hash: str
    minner_uuid: UUID
    coinbase: Coinbase

    def __init__(self, id: int, previous_hash: str, coinbase: Coinbase):
        self.id = id
        self.transactions = []
        self.nonce = 0
        self.previous_hash = previous_hash
        self.merkle_tree = MerkleTree([[]])
        self.coinbase = coinbase
        self.minner_uuid = None
    
    def hash(self) -> str:
        data = self.to_json()
        self.current_hash = custom_hash_md5(json.dumps(data, sort_keys=True))

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def transfer_coinbase(self):
        # OUT OF RANGE!
        pass

    def transfer_transaction(self):
        pass
    
    def to_json(self):
        return {
            "nonce": self.nonce,
            "merkle_root": self.merkle_tree.root,
            "transactions": [trans.to_json_str() for trans in self.transactions]
        }
