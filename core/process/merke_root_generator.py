from core.models.transaction import Transaction
from core.models.merkle_tree import MerkleTree
from core.helpers import custom_hash_sha512
from core.base_class import BaseClass


class MerkleTreeGenerator(BaseClass):
    merkle_tree: MerkleTree
    root: str

    def __init__(self, merkle_tree: MerkleTree):
        self.merkle_tree = merkle_tree

    def handle(self, transaction: Transaction):

        self.merkle_tree.nodes[0].append(transaction.hash())
        self.calculate_last_parent()
        self.merkle_tree.root = self.merkle_tree.nodes[-1][0]

        return self

    def hash_sons(self, son_1: str, son_2: str) -> str:
        result = custom_hash_sha512(f"{son_1}{son_2}")
        return result

    def calculate_last_parent(self, pos: int = 0):
        if len(self.merkle_tree.nodes) < pos:
            self.merkle_tree.nodes.append([])

        if len(self.merkle_tree.nodes[pos]) % 2 != 0:
            return

        last_pair = self.merkle_tree.nodes[pos][-2:]

        new_pos = pos + 1

        if len(self.merkle_tree.nodes) <= new_pos:
            self.merkle_tree.nodes.append([])

        new_node = self.hash_sons(*last_pair)
        self.merkle_tree.nodes[new_pos].append(new_node)

        self.calculate_last_parent(new_pos)
