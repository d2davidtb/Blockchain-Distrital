from uuid import UUID
from typing import List

from core.models.block import Block
from core.models.transaction import Transaction
from core.models.coinbase import Coinbase
from core.models.nodes import Nodes


class GenesisBlock(Block):
    def __init__(self, nodes):
        super().__init__(0, "0"*64, Coinbase(nodes.get(0), 100))
        self.transactions = []


class BlockChain:
    blocks: List[Block]

    def __init__(self, initial_nodes: Nodes):
        self.blocks = [
            GenesisBlock(initial_nodes)
        ]

    def add_block(self, block: Block):
        self.blocks.append(block)
