from fastapi.testclient import TestClient


def test_get_chain(blockchain_client: TestClient):
    response = blockchain_client.get("/chain")
    assert response.status_code == 200
    data = response.json()
    assert "chain" in data
    assert "length" in data
    assert data["length"] == 1  # Genesis block


def test_mine(blockchain_client: TestClient):
    response = blockchain_client.get("/mine")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "New block created"

    # Confirm chain length changed
    response = blockchain_client.get("/chain")
    assert response.json()["length"] == 2


def test_new_transaction_invalid(blockchain_client: TestClient):
    response = blockchain_client.post(
        "/transactions/new",
        data={
            "confirmation_sender_public_key": "s",
            "confirmation_recipient_public_key": "r",
            "transaction_signature": "invalid",
            "confirmation_amount": "100",
        },
    )
    # signature verification fails
    assert response.status_code == 406
    assert response.json()["message"] == "Invalid transaction/signature"


def test_register_node(blockchain_client: TestClient):
    response = blockchain_client.get("/nodes/get")
    assert len(response.json()["nodes"]) == 0

    response = blockchain_client.post(
        "/nodes/register", data={"nodes": "127.0.0.1:5002, 127.0.0.1:5003"}
    )
    assert response.status_code == 200
    assert len(response.json()["total_nodes"]) == 2

    response = blockchain_client.get("/nodes/get")
    assert len(response.json()["nodes"]) == 2
