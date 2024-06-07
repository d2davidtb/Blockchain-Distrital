from typing import List
from uuid import UUID

from core.models.merkle_tree import MerkleTree
from core.models.coinbase import Coinbase
from core.models.transaction import Transaction

class Block:
    id: int
    merkle_tree: MerkleTree
    transactions: List[Transaction]
    nonce: int
    previous_hash: str
    hash: str
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

    def hash() -> str:
        # HASH usando MD5 de los bloques: Nonce + Merkle Root + Transacciones, tenga 3 ceros en el inicio
        pass

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def transfer_coinbase(self):
        pass

    def transfer_transaction(self):
        pass
