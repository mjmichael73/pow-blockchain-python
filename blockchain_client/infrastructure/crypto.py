import binascii
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

class CryptoService:
    @staticmethod
    def generate_wallet() -> dict:
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()

        return {
            "private_key": binascii.hexlify(private_key.export_key(format("DER"))).decode("ascii"),
            "public_key": binascii.hexlify(public_key.export_key(format("DER"))).decode("ascii"),
        }

    @staticmethod
    def sign_transaction(sender_private_key: str, transaction_dict: dict) -> str:
        private_key = RSA.importKey(binascii.unhexlify(sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(transaction_dict).encode("utf8"))
        return binascii.hexlify(signer.sign(h)).decode("ascii")
