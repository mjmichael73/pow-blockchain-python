from .transaction import Transaction
from ..infrastructure.crypto import CryptoService

class WalletService:
    def __init__(self, crypto_service: CryptoService):
        self.crypto_service = crypto_service

    def create_wallet(self) -> dict:
        return self.crypto_service.generate_wallet()

    def create_and_sign_transaction(self, sender_public_key: str, sender_private_key: str, 
                                     recipient_public_key: str, amount: float) -> dict:
        transaction = Transaction(sender_public_key, recipient_public_key, amount)
        signature = self.crypto_service.sign_transaction(sender_private_key, transaction.to_dict())
        
        return {
            "transaction": transaction.to_dict(),
            "signature": signature
        }
