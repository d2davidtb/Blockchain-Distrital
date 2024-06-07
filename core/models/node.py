from uuid import UUID
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from core.models.transaction import Transaction
from core.models.blockchain import BlockChain
from core.models.block import Block
from core.models.nodes import Nodes
from core.helpers import custom_hash_sha512_obj, custom_hash_sha512
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

    def get_closed_block(self):
        last_block = self.get_last_block()
        if len(last_block.transactions) != 16:
            last_block = self.block_chain.blocks[-2]
        return last_block

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
            # OUT OF RANGE! Diffusion
            is_valid = self.block_verification()
            if is_valid:
                self.block_filling_out()
                # OUT OF RANGE! Coinbase transaction

        return True

    def minnig(self):
        pending_block: Block = self.get_closed_block()
        pending_block.hash()
        data = pending_block.to_json()
        block_hash = custom_hash_md5(json.dumps(data, sort_keys=True))

        proof_of_work = False
        while not proof_of_work:
            if "000" == block_hash[:3]:
                print("Proof of work found: Aleluya")
                # OUT OF RANGE!: blocks Block
                pending_block.minner_uuid = self.uuid
                proof_of_work = True
                break

            data["nonce"] += 1
            block_hash = custom_hash_md5(json.dumps(data, sort_keys=True))

    def block_verification(self) -> bool:
        closed_block: Block = self.get_closed_block()
        closed_block.hash()
        data = {
            "nonce": closed_block.nonce,
            "merkle_root": closed_block.merkle_tree.root,
            "transactions": [trans.to_json_str() for trans in closed_block.transactions]
        }
        block_hash = custom_hash_md5(json.dumps(data, sort_keys=True))
        if closed_block.current_hash == block_hash:
            return True

        # OUT OF RANGE! Continue listening
        return False
    
    def block_filling_out(self):
        module = 1640
        closed_block: Block = self.get_closed_block()
        open_block: Block = self.get_last_block()
        if open_block.id % module == 0:
            open_block.coinbase = open_block.coinbase
        else:
            open_block.coinbase.value = open_block.coinbase.value * 0.75

        closed_block.hash()
        open_block.previous_hash = custom_hash_sha512(closed_block.current_hash)
