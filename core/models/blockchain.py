from uuid import UUID
from typing import List

from core.models.block import Block
from core.models.transaction import Transaction
from core.models.coinbase import Coinbase
from core.models.nodes import Nodes


class GenesisBlock(Block):
    def __init__(self, nodes):
        super().__init__(0, "0"*64, Coinbase(nodes[0], 100))
        self.transactions = [
            Transaction(nodes[0].uuid, nodes[1].uuid, 10),
            Transaction(nodes[0].uuid, nodes[2].uuid, 10),
            Transaction(nodes[0].uuid, nodes[3].uuid, 10),
            Transaction(nodes[0].uuid, nodes[4].uuid, 10),
            Transaction(nodes[0].uuid, nodes[5].uuid, 10),
            Transaction(nodes[0].uuid, nodes[6].uuid, 10),
            Transaction(nodes[0].uuid, nodes[7].uuid, 10),
            Transaction(nodes[0].uuid, nodes[8].uuid, 10),
            Transaction(nodes[0].uuid, nodes[9].uuid, 10),
        ]


class BlockChain:
    blocks: List[Block]

    def __init__(self, initial_nodes: Nodes):
        self.blocks = [
            GenesisBlock(initial_nodes.nodes)
        ]

    def add_block(self, block: Block):
        self.blocks.append(block)
