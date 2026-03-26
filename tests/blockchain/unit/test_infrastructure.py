from blockchain.infrastructure.crypto import CryptoService
from blockchain_client.infrastructure.crypto import CryptoService as ClientCryptoService
from collections import OrderedDict


def test_signature_verification():
    # 1. Generate keys using Client service
    wallet = ClientCryptoService.generate_wallet()
    pub = wallet["public_key"]
    priv = wallet["private_key"]

    # 2. Sign a transaction
    tx_dict = OrderedDict(
        {"sender_public_key": pub, "recipient_public_key": "recipient", "amount": 5.0}
    )
    sig = ClientCryptoService.sign_transaction(priv, tx_dict)

    # 3. Verify using Node service
    assert CryptoService.verify_signature(pub, sig, tx_dict) is True

    # 4. Verify failure with modified data
    tx_dict_modified = tx_dict.copy()
    tx_dict_modified["amount"] = 10.0
    assert CryptoService.verify_signature(pub, sig, tx_dict_modified) is False

    # 5. Verify failure with wrong signature
    assert CryptoService.verify_signature(pub, "wrong_sig", tx_dict) is False
