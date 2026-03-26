from typing import List, Any, Dict, Optional
import os
from time import time
from uuid import uuid4
from collections import OrderedDict
from ..domain.entities import Block, Transaction
from ..domain.logic import BlockchainLogic
from ..infrastructure.crypto import CryptoService
from ..infrastructure.p2p import P2PClient

# Constants
MINING_SENDER = os.getenv("MINING_SENDER", "The Blockchain")
MINING_REWARD = float(os.getenv("MINING_REWARD", "1"))
MINING_DIFFICULTY = int(os.getenv("MINING_DIFFICULTY", "2"))

class BlockchainService:
    def __init__(self, crypto_service: CryptoService, p2p_client: P2PClient):
        self.crypto_service = crypto_service
        self.p2p_client = p2p_client
        self.transactions: List[Transaction] = []
        self.chain: List[Block] = []
        self.node_id = str(uuid4()).replace("-", "")
        
        # Create genesis block
        self._create_block(nonce=0, previous_hash="00")

    def _create_block(self, nonce: int, previous_hash: str) -> Block:
        block = Block(
            block_number=len(self.chain) + 1,
            timestamp=time(),
            transactions=list(self.transactions),
            nonce=nonce,
            previous_hash=previous_hash
        )
        self.transactions = []
        self.chain.append(block)
        return block

    def submit_transaction(self, sender_public_key: str, recipient_public_key: str, signature: str, amount: Any) -> Optional[int]:
        transaction = Transaction(
            sender_public_key=sender_public_key,
            recipient_public_key=recipient_public_key,
            amount=amount,
            signature=signature
        )

        if sender_public_key == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            if self.crypto_service.verify_signature(sender_public_key, signature, transaction.to_dict()):
                self.transactions.append(transaction)
                return len(self.chain) + 1
            return None

    def mine(self) -> Dict[str, Any]:
        last_block = self.chain[-1]
        nonce = BlockchainLogic.proof_of_work(
            [t.to_dict() for t in self.transactions],
            last_block.to_dict(),
            MINING_DIFFICULTY
        )

        # Mining reward
        self.submit_transaction(
            sender_public_key=MINING_SENDER,
            recipient_public_key=self.node_id,
            signature="",
            amount=MINING_REWARD
        )

        previous_hash = BlockchainLogic.hash_block(last_block.to_dict())
        block = self._create_block(nonce, previous_hash)
        return block.to_dict()

    def resolve_conflicts(self) -> bool:
        new_chain = None
        max_length = len(self.chain)

        for node in self.p2p_client.nodes:
            data = self.p2p_client.fetch_chain(node)
            if data:
                length = data["length"]
                chain_data = data["chain"]

                if length > max_length and self._valid_chain(chain_data):
                    max_length = length
                    new_chain = chain_data

        if new_chain:
            # Convert chain_data back to Block entities
            self.chain = []
            for b in new_chain:
                txs = [Transaction(**t) for t in b["transactions"]]
                self.chain.append(Block(
                    block_number=b["block_number"],
                    timestamp=b["timestamp"],
                    transactions=txs,
                    nonce=b["nonce"],
                    previous_hash=b["previous_hash"]
                ))
            return True
        return False

    def _valid_chain(self, chain_data: List[Dict[str, Any]]) -> bool:
        last_block_data = chain_data[0]
        current_index = 1

        while current_index < len(chain_data):
            block_data = chain_data[current_index]
            if block_data["previous_hash"] != BlockchainLogic.hash_block(last_block_data):
                return False

            # Validate transactions proof
            transactions = block_data["transactions"][:-1]
            transaction_elements = ["sender_public_key", "recipient_public_key", "amount"]
            formatted_txs = [
                OrderedDict((k, tx[k]) for k in transaction_elements)
                for tx in transactions
            ]

            if not BlockchainLogic.valid_proof(
                formatted_txs, block_data["previous_hash"], block_data["nonce"], MINING_DIFFICULTY
            ):
                return False

            last_block_data = block_data
            current_index += 1
        return True
