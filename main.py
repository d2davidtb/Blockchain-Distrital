from typing import Tuple
from uuid import uuid4

from Crypto.PublicKey import RSA

from core.models.myself import Myself
from core.models.node import Nodes, Node


def init() -> Tuple[Myself, Nodes]:
    myself = Myself()
    
    nodes = Nodes()
    nodes.add_node(myself)
    for _ in range(9):
        key = RSA.generate(1024)
        public_key = key.publickey().export_key()
        nodes.add_node(Node(uuid4(), public_key, 10))

    for node in nodes.nodes:
        node.set_nodes(nodes)

    return myself, nodes

def run_flow():
    myself, nodes = init()
    transaction = myself.create_transaction(nodes.get(1).uuid, 2)

    is_valid = nodes.get(2).verify_transaction(transaction)
    print("is_valid", is_valid)

    

    # actor creation = ActorCreation()
    # Node creation = NodeCreation()
    # transaction_creation = TransactionCreation()
    # transaction_verification = TransactionVerification()
    # minning = Minning()
    # generator = MerkleTreeGenerator([t, t2]).handle()
    # block_verification = BlockVerification()

if __name__ == "__main__":
    run_flow()
