from typing import List


class MerkleTree:
    nodes: List[List[str]]
    root: str

    def __init__(self, nodes: list):
        self.nodes = nodes
