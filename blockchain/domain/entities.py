from dataclasses import dataclass, field
from typing import List, Optional, Set
from time import time
from collections import OrderedDict

@dataclass
class Transaction:
    sender_public_key: str
    recipient_public_key: str
    amount: float
    signature: Optional[str] = None

    def to_dict(self):
        return OrderedDict({
            "sender_public_key": self.sender_public_key,
            "recipient_public_key": self.recipient_public_key,
            "amount": self.amount,
        })

@dataclass
class Block:
    block_number: int
    timestamp: float
    transactions: List[Transaction]
    nonce: int
    previous_hash: str

    def to_dict(self):
        return {
            "block_number": self.block_number,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
        }
