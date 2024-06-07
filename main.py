from typing import Tuple
from uuid import uuid4

from Crypto.PublicKey import RSA

from core.models.myself import Myself
from core.models.node import Nodes, Node
from core.models.transaction import Transaction
from core.models.block import Block


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

    def __set_first_transactions(self):
        # Creating and Sign
        print("Creating initial transactions...")
        for i in range(1, 10):
            print("| Create and verify by all. Value 10")
            transaction = self.myself.create_transaction(self.nodes.get(i).uuid, 10)
            self.__verify_transaction_by_all(transaction)
        print("...Initial transactions created")

    def __create_enough_transactions(self):
        # Creating and Sign
        print("Creating initial transactions...")
        for i in range(0, 7):
            print("| Create and verify by all. Value 1")
            transaction = self.myself.create_transaction(self.nodes.get(i).uuid, 1)
            self.__verify_transaction_by_all(transaction)
        print("...Other transactions created")

    def __verify_transaction_by_all(self, transaction: Transaction):
        for node in self.nodes.nodes:
            # Verify
            is_valid = node.verify_transaction(self.nodes, transaction)
            if not is_valid:
                # OUT OF RANGE!: Reject and diffuse
                pass


if __name__ == "__main__":
    Flow().handle()
