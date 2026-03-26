import json
import hashlib
from typing import List, Any
from .entities import Block, Transaction

class BlockchainLogic:
    @staticmethod
    def valid_proof(transactions: List[Any], last_hash: str, nonce: int, difficulty: int) -> bool:
        guess = (str(transactions) + str(last_hash) + str(nonce)).encode("utf8")
        h = hashlib.new("sha256")
        h.update(guess)
        guess_hash = h.hexdigest()
        return guess_hash[:difficulty] == "0" * difficulty

    @staticmethod
    def hash_block(block_dict: dict) -> str:
        block_string = json.dumps(block_dict, sort_keys=True).encode("utf8")
        h = hashlib.new("sha256")
        h.update(block_string)
        return h.hexdigest()

    @staticmethod
    def proof_of_work(transactions: List[Any], last_block_dict: dict, difficulty: int) -> int:
        last_hash = BlockchainLogic.hash_block(last_block_dict)
        nonce = 0
        # This is the heavy lifting
        while BlockchainLogic.valid_proof(transactions, last_hash, nonce, difficulty) is False:
            nonce += 1
        return nonce
