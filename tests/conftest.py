import pytest
from fastapi.testclient import TestClient
from blockchain.main import create_app as create_blockchain_app
from blockchain_client.main import create_app as create_client_app


@pytest.fixture
def blockchain_app():
    return create_blockchain_app()


@pytest.fixture
def blockchain_client(blockchain_app):
    return TestClient(blockchain_app)


@pytest.fixture
def wallet_app():
    return create_client_app()


@pytest.fixture
def wallet_client(wallet_app):
    return TestClient(wallet_app)
