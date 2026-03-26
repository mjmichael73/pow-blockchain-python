from blockchain.domain.logic import BlockchainLogic


def test_hash_block():
    block = {
        "block_number": 1,
        "timestamp": 123456789.0,
        "transactions": [],
        "nonce": 0,
        "previous_hash": "00",
    }
    h1 = BlockchainLogic.hash_block(block)
    h2 = BlockchainLogic.hash_block(block)

    assert len(h1) == 64
    assert h1 == h2  # Deterministic


def test_valid_proof():
    transactions = []
    last_hash = "abc"
    difficulty = 2

    # Test a clearly invalid nonce
    assert (
        BlockchainLogic.valid_proof(
            transactions, last_hash, nonce=0, difficulty=difficulty
        )
        is False
    )

    # Test a valid nonce (found by trial)
    # This is a bit slow but ensures logic works
    nonce = BlockchainLogic.proof_of_work(transactions, {"dummy": "block"}, difficulty)
    # Wait, proof_of_work calls hash_block on the dict
    last_block = {"data": "test"}
    last_hash = BlockchainLogic.hash_block(last_block)
    nonce = 0
    while not BlockchainLogic.valid_proof(transactions, last_hash, nonce, difficulty):
        nonce += 1

    assert (
        BlockchainLogic.valid_proof(transactions, last_hash, nonce, difficulty) is True
    )


def test_proof_of_work():
    transactions = []
    last_block = {"block_number": 1, "nonce": 0}
    difficulty = 1  # Keep it fast for tests

    nonce = BlockchainLogic.proof_of_work(transactions, last_block, difficulty)
    last_hash = BlockchainLogic.hash_block(last_block)

    assert (
        BlockchainLogic.valid_proof(transactions, last_hash, nonce, difficulty) is True
    )
