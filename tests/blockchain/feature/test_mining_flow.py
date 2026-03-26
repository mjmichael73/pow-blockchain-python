from fastapi.testclient import TestClient


def test_full_mining_flow(blockchain_client: TestClient, wallet_client: TestClient):
    """
    Scenario:
    1. Create a wallet
    2. Create a signed transaction
    3. Submit it to the node
    4. Verify it's in the mempool
    5. Mine a block
    6. Verify it's on the chain
    """
    # 1. Create a wallet
    wallet = wallet_client.get("/wallet/new").json()
    pub = wallet["public_key"]
    priv = wallet["private_key"]

    # 2. Generate transaction
    tx_data = wallet_client.post(
        "/generate/transaction",
        data={
            "sender_public_key": pub,
            "sender_private_key": priv,
            "recipient_public_key": "recipient_addr",
            "amount": "500",
        },
    ).json()

    # 3. Submit to node
    response = blockchain_client.post(
        "/transactions/new",
        data={
            "confirmation_sender_public_key": tx_data["transaction"][
                "sender_public_key"
            ],
            "confirmation_recipient_public_key": tx_data["transaction"][
                "recipient_public_key"
            ],
            "transaction_signature": tx_data["signature"],
            "confirmation_amount": tx_data["transaction"]["amount"],
        },
    )
    assert response.status_code == 201

    # 4. Verify in mempool
    response = blockchain_client.get("/transactions/get")
    assert len(response.json()["transactions"]) == 1

    # 5. Mine block
    response = blockchain_client.get("/mine")
    assert response.status_code == 200

    # 6. Verify chain
    response = blockchain_client.get("/chain")
    chain = response.json()["chain"]
    assert len(chain) == 2
    assert len(chain[1]["transactions"]) == 2  # 1 User + 1 Reward
