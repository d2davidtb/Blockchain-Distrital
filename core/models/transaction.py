import json
from uuid import UUID, uuid4

from core.helpers import custom_hash_sha512


class Transaction:
    uuid: UUID
    sender_id: str
    receiver_id: str
    value: float
    signature: str

    def __init__(
        self,
        sender_uuid: UUID = "",
        receiver_uuid: UUID = "",
        value: float = 0.0,
    ):
        self.uuid = uuid4()
        self.sender_uuid = sender_uuid
        self.receiver_uuid = receiver_uuid
        self.value = value

    def to_json_str(self) -> str:
        data = dict(
            uuid=str(self.uuid),
            sender_uuid=str(self.sender_uuid),
            receiver_uuid=str(self.receiver_uuid),
            value=self.value,
        )
        return json.dumps(data, sort_keys=True)
    
    def hash(self):
        return custom_hash_sha512(self.to_json_str())

    def set_signature(self, signature: str):
        self.signature = signature

