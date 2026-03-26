from collections import OrderedDict

class Transaction:
    def __init__(self, sender_public_key: str, recipient_public_key: str, amount: float):
        self.sender_public_key = sender_public_key
        self.recipient_public_key = recipient_public_key
        self.amount = amount

    def to_dict(self) -> OrderedDict:
        return OrderedDict({
            "sender_public_key": self.sender_public_key,
            "recipient_public_key": self.recipient_public_key,
            "amount": self.amount,
        })
