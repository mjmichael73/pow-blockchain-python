from fastapi.testclient import TestClient


def test_wallet_new(wallet_client: TestClient):
    response = wallet_client.get("/wallet/new")
    assert response.status_code == 200
    data = response.json()
    assert "public_key" in data
    assert "private_key" in data


def test_generate_transaction(wallet_client: TestClient):
    # 1. New wallet
    wallet = wallet_client.get("/wallet/new").json()

    # 2. Generate transaction
    response = wallet_client.post(
        "/generate/transaction",
        data={
            "sender_public_key": wallet["public_key"],
            "sender_private_key": wallet["private_key"],
            "recipient_public_key": "someone",
            "amount": "123.45",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction" in data
    assert "signature" in data
    assert data["transaction"]["amount"] == 123.45


def test_template_rendering(wallet_client: TestClient):
    # Testing main routes
    assert wallet_client.get("/").status_code == 200
    assert wallet_client.get("/make/transaction").status_code == 200
    assert wallet_client.get("/view/transactions").status_code == 200
