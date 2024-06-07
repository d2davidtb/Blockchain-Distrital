from uuid import UUID


class Nodes:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_node(self, uuid: UUID):
        return next(filter(lambda node: node.uuid == uuid, self.nodes), None)

    def get(self, index: int):
        return self.nodes[index]
