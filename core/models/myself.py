from typing import List
from uuid import UUID, uuid4

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from core.models.block import Block
from core.models.blockchain import BlockChain
from core.models.transaction import Transaction
from core.models.node import Node
from core.helpers import custom_hash_sha512_obj


class Myself(Node):
    uuid: UUID
    public_key: str
    private_key: str
    block_chain: List[Block]

    def __init__(self):
        self.uuid = uuid4()
        key = RSA.generate(2048)
        self.public_key = key.publickey().export_key()
        self.private_key = key.export_key()
        super().__init__(self.uuid, self.public_key, 100)

    def create_transaction(self, receiver_uuid: UUID, value: float) -> Transaction:
        transaction = Transaction(
            sender_uuid=self.uuid,
            receiver_uuid=receiver_uuid,
            value=value,
        )
        transaction.set_signature(
            self.sign_transaction(transaction)
        )
        return transaction

    def sign_transaction(self, transaction: Transaction) -> bytes:
        hash_data = custom_hash_sha512_obj(transaction.to_json_str())
        with open("private.pem", "wb") as f:
            f.write(self.private_key)

        key = RSA.import_key(open('private.pem').read())
        signature = pkcs1_15.new(key).sign(hash_data)
        return signature
