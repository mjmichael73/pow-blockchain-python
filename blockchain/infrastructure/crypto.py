import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

class CryptoService:
    @staticmethod
    def verify_signature(sender_public_key: str, signature: str, transactions_dict: dict) -> bool:
        try:
            public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
            verifier = PKCS1_v1_5.new(public_key)
            h = SHA.new(str(transactions_dict).encode("utf8"))
            return verifier.verify(h, binascii.unhexlify(signature))
        except (ValueError, TypeError, binascii.Error):
            return False
