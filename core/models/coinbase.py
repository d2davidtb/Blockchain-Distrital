from uuid import UUID


class Coinbase:
    value: float
    receiver_uuid: UUID

    def __init__(self, receiver_uuid: UUID, value: float):
        self.receiver_uuid = receiver_uuid
        self.value = value
