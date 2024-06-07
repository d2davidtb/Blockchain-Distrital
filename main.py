from typing import Tuple
from uuid import uuid4

from Crypto.PublicKey import RSA

from core.models.myself import Myself
from core.models.node import Nodes, Node
from core.models.transaction import Transaction


def init() -> Tuple[Myself, Nodes]:
    myself = Myself()
    
    nodes = Nodes()
    nodes.add_node(myself)
    for _ in range(9):
        key = RSA.generate(1024)
        public_key = key.publickey().export_key()
        nodes.add_node(Node(uuid4(), public_key, 10))

    for i, node in enumerate(nodes.nodes):
        node.set_nodes(nodes)
        nodes.nodes[i] = node

    return myself, nodes

class Flow:
    
    def __init__(self):
        self.myself, self.nodes = init()
        
    def handle(self):
        self.__set_first_transactions()
        self.__create_enough_transactions()
        print("blocks", self.myself.block_chain.blocks)
        print("last block transactions", self.myself.block_chain.blocks[-1].transactions)
    
    def __set_first_transactions(self):
        # Creating and Sign
        for i in range(1, 10):
            transaction = self.myself.create_transaction(self.nodes.get(i).uuid, 10)
            self.verify_transaction_by_all(transaction)

    def __create_enough_transactions(self):
        # Creating and Sign
        for i in range(0, 7):
            transaction = self.myself.create_transaction(self.nodes.get(i).uuid, 1)
            self.verify_transaction_by_all(transaction)
                
    def verify_transaction_by_all(self, transaction: Transaction):
        for node in self.nodes.nodes:
            # Verify
            is_valid = node.verify_transaction(self.nodes, transaction)


if __name__ == "__main__":
    Flow().handle()
