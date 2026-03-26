from blockchain.domain.entities import Transaction, Block
from collections import OrderedDict
from time import time


def test_transaction_to_dict():
    tx = Transaction(
        sender_public_key="sender",
        recipient_public_key="recipient",
        amount=10.0,
        signature="sig",
    )
    tx_dict = tx.to_dict()

    assert isinstance(tx_dict, OrderedDict)
    assert tx_dict["sender_public_key"] == "sender"
    assert tx_dict["recipient_public_key"] == "recipient"
    assert tx_dict["amount"] == 10.0
    assert (
        "signature" not in tx_dict
    )  # signature is handled separately in blockchain logic


def test_block_to_dict():
    tx = Transaction("s", "r", 1.0)
    block = Block(
        block_number=1,
        timestamp=time(),
        transactions=[tx],
        nonce=100,
        previous_hash="00",
    )
    block_dict = block.to_dict()

    assert block_dict["block_number"] == 1
    assert len(block_dict["transactions"]) == 1
    assert block_dict["transactions"][0]["sender_public_key"] == "s"
    assert block_dict["nonce"] == 100
    assert block_dict["previous_hash"] == "00"
