# Proof of Work Blockchain in Python

A robust implementation of a Proof of Work (PoW) Blockchain and a corresponding Blockchain Client (Wallet) written in Python using **FastAPI**, **Clean Architecture** principles, and **PyCryptodome**.

This project serves as an educational tool to understand the underlying mechanisms of a blockchain network, including blocks, transactions, public-key cryptography, proof of work, and consensus, all while demonstrating modern software engineering practices.

## 🏛️ Architecture

The project is built following **Clean Architecture** principles to ensure separation of concerns, testability, and maintainability.

### Layers:
1.  **Domain**: Core entities (`Block`, `Transaction`) and pure business logic (hashing, proof of work validation).
2.  **Application**: Use cases that coordinate domain logic (e.g., `BlockchainService` for mining, `WalletService` for signing).
3.  **Infrastructure**: External implementations such as Cryptography (RSA/SHA256) and P2P Networking (HTTP clients).
4.  **API (Delivery)**: FastAPI routers and template handlers that interface with the user.

### Components:
-   **Blockchain Node (`/blockchain`)**: Handles mining, mempool management, and P2P consensus.
-   **Blockchain Client (`/blockchain_client`)**: A wallet UI for generating RSA keys, creating signed transactions, and viewing the chain.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (Recommended)

### Installation

1.  Clone the repository and navigate to the root directory.
2.  **Configuration**: Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    Adjust settings like `MINING_DIFFICULTY` or `MINING_REWARD` in `.env` as needed.

## 🛠️ Running the Application

### Option 1: Using Docker Compose (Recommended)

In the root directory, run:
```bash
docker compose up --build
```
The services will be available at:
- **Blockchain Node 1**: `http://localhost:5001`
- **Blockchain Node 2**: `http://localhost:5002` (for P2P sync testing)
- **Blockchain Client**: `http://localhost:8081`

### Option 2: Running Locally

1.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the components in separate terminals:
    **Node**: `python blockchain/main.py -p 5001`
    **Client**: `python blockchain_client/main.py -p 8081`

## 🧪 Manual Testing Flow

1.  Open the **Blockchain Client** (`http://localhost:8081`) and generate a new wallet. **Copy the keys**.
2.  Go to "Make Transaction", enter your keys, a recipient address, and an amount. Click "Generate Transaction".
3.  Submit the transaction to a node (e.g., `http://localhost:5001`).
4.  Open the **Blockchain Node 1** UI (`http://localhost:5001`) and navigate to the Mining section.
5.  Click "Mine" to seal the transaction into a new block.
6.  (Optional) Run Node 2, register Node 1, and use the "Consensus" feature to sync Node 2 with Node 1's longer chain.

---

## 🗺️ Roadmap / TODO (Production Readiness)

To transition this educational project into a production-ready blockchain, the following enhancements are recommended:

### Phase 1: Persistence & Reliability
- [ ] **Database Persistence**: Replace in-memory storage with a persistent key-value store (e.g., RocksDB or LevelDB) or a relational database (PostgreSQL) to survive restarts.
- [ ] **Automated Testing**: Implement a comprehensive suite of unit and integration tests using `pytest` to ensure core logic (PoW, validation) is bug-free.
- [ ] **Logging & Observability**: Add structured logging and export metrics (e.g., hash rate, block time) for monitoring via Prometheus/Grafana.

### Phase 2: Network & Security
- [ ] **Gossip Protocol**: Implement a real P2P discovery mechanism (like a Gossip protocol) so nodes can discover each other automatically without manual registration.
- [ ] **Real-time Broadcasting**: Switch from a "pull-based" consensus to a "push-based" system where new blocks and transactions are broadcasted instantly to all peers.
- [ ] **Standardized Encryption**: Secure peer communication using TLS/SSL and implement rate-limiting to prevent DDoS attacks.
- [ ] **HD Wallets**: Implement Hierarchical Deterministic (HD) wallets (BIP-32/39/44) for better user key management.

### Phase 3: Scalability & Performance
- [ ] **Merkle Trees**: Use Merkle Trees for transaction verification within blocks to allow for SPV (Simplified Payment Verification) and more efficient state checks.
- [ ] **Transaction Fees & Mempool**: Add logic for transaction prioritization based on fees to handle network congestion.
- [ ] **Difficulty Retargeting**: Implement an algorithm (like the one used in Bitcoin) to adjust the mining difficulty dynamically based on the network's total hash rate.
- [ ] **Asynchronous Mining**: Move the Proof of Work heavy-lifting to background worker processes to prevent blocking the API thread.

---

## 📜 License
This project is open-source and available under the terms of the MIT License.