from uuid import UUID
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from core.models.transaction import Transaction
from core.models.blockchain import BlockChain
from core.models.block import Block
from core.models.nodes import Nodes
from core.helpers import custom_hash_sha512_obj
from core.process.merke_root_generator import MerkleTreeGenerator
from core.helpers import custom_hash_md5


class Node:

    def __init__(self, uuid: UUID, public_key: str, balance: float):
        self.uuid = uuid
        self.public_key = public_key
        self.balance = balance

    def set_nodes(self, nodes: Nodes):
        self.block_chain = BlockChain(nodes)

    def get_last_block(self):
        return self.block_chain.blocks[-1]

    def verify_transaction(self, nodes, transaction: Transaction) -> bool:
        # Verify signature
        node = nodes.get_node(transaction.sender_uuid)
        public_key = node.public_key
        hash_data = custom_hash_sha512_obj(transaction.to_json_str())
        with open("public.pem", "wb") as f:
            f.write(public_key)

        key = RSA.import_key(open('public.pem').read())

        try:
            pkcs1_15.new(key).verify(hash_data, transaction.signature)
        except ValueError:
            return False

        # OUT OF RANGE!: Balance verification
        if node.balance < transaction.value:
            return False

        # OUT OF RANGE!: Broadcast to update node balance
        # node.balance = node.balance - transaction.value

        # Add transaction to open block
        self.block_chain.blocks[-1].add_transaction(transaction)

        # Update Merkletree
        self.block_chain.blocks[-1].merkle_tree = MerkleTreeGenerator(
            self.block_chain.blocks[-1].merkle_tree
        ).handle(transaction).merkle_tree

        # Add new block if previous is full
        if len(self.block_chain.blocks[-1].transactions) == 16:
            self.block_chain.add_block(
                Block(
                    len(self.block_chain.blocks),
                    "",
                    self.block_chain.blocks[-1].coinbase,
                )
            )
            self.minnig()

        return True

    def minnig(self):
        last_block = self.get_last_block()
        if len(last_block.transactions) != 16:
            last_block = self.block_chain.blocks[-2]

        data = {"nonce": last_block.nonce, "merkle_root": last_block.merkle_tree.root, "transactions": last_block.transactions}
        data["transactions"] = [trans.to_json_str() for trans in last_block.transactions]

        block_hash = custom_hash_md5(json.dumps(data, sort_keys=True))
        proof_of_work = False

        while not proof_of_work:
            if "0000" == block_hash[:4]:
                print("Prueba de trabajo encontrada Aleluya")
                proof_of_work = True
            else:
                data["nonce"] += 1
                block_hash = custom_hash_md5(json.dumps(data, sort_keys=True))

        print("Hash del de prueba de trabajo", block_hash)