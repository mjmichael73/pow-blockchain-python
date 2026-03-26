from blockchain_client.application.wallet_service import WalletService
from blockchain_client.infrastructure.crypto import CryptoService
from collections import OrderedDict


def test_wallet_creation():
    service = WalletService(CryptoService())
    wallet = service.create_wallet()

    assert "public_key" in wallet
    assert "private_key" in wallet
    assert len(wallet["public_key"]) > 0


def test_transaction_creation():
    service = WalletService(CryptoService())
    wallet = service.create_wallet()
    pub = wallet["public_key"]
    priv = wallet["private_key"]

    result = service.create_and_sign_transaction(pub, priv, "recipient", 50.5)

    assert "transaction" in result
    assert "signature" in result
    assert result["transaction"]["amount"] == 50.5
    assert isinstance(result["transaction"], OrderedDict)
