# ⛓️ Proof of Work Blockchain — Python

A full-stack implementation of a **Proof of Work (PoW) Blockchain** and a **Blockchain Wallet Client** written in Python.

Built with **FastAPI**, **Clean Architecture**, **PyCryptodome**, and **Docker** — serving both as an educational reference and as a foundation for further production hardening.

---

## Table of Contents

- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [How to Run](#-how-to-run)
- [API Reference](#-api-reference)
- [How to Test](#-how-to-test)
- [Test Flow (E2E Walkthrough)](#-test-flow-e2e-walkthrough)
- [TODO — Production Readiness](#-todo--production-readiness)
- [Known Bugs & Required Fixes](#-known-bugs--required-fixes)
- [License](#-license)

---

## 🏛️ Architecture

The project follows **Clean Architecture** principles across two independent FastAPI services:

```
┌──────────────────────────────────────────────────────────────┐
│                         Blockchain Node                       │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  API     │→ │  Application │→ │  Domain                │  │
│  │ (Routes) │  │  (Services)  │  │  (Entities + Logic)    │  │
│  └──────────┘  └──────────────┘  └────────────────────────┘  │
│                        ↓                                      │
│               ┌─────────────────┐                            │
│               │  Infrastructure  │                            │
│               │  (Crypto + P2P)  │                            │
│               └─────────────────┘                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                       Blockchain Client (Wallet)              │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  API     │→ │  Wallet      │→ │  Domain (Transaction)  │  │
│  │ (Routes) │  │  Service     │  └────────────────────────┘  │
│  └──────────┘  └──────────────┘                              │
│                        ↓                                      │
│               ┌──────────────────┐                           │
│               │  Infrastructure  │                            │
│               │  (RSA Crypto)    │                            │
│               └──────────────────┘                           │
└──────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Purpose |
|---|---|
| **Domain** | Pure business logic: `Block`, `Transaction` dataclasses; `BlockchainLogic` (SHA-256 hashing, PoW validation) |
| **Application** | Orchestration use-cases: `BlockchainService` (mine, submit tx, resolve conflicts), `WalletService` (generate wallet, sign tx) |
| **Infrastructure** | Adapters: `CryptoService` (RSA key gen & PKCS#1 v1.5 signature verify/sign), `P2PClient` (HTTP-based chain fetch) |
| **API** | FastAPI routers — thin delivery layer, delegates everything to application services via dependency injection |

### Services

| Service | Port | Role |
|---|---|---|
| `blockchain` | `5001` (default) | Full blockchain node: mempool, mining, P2P |
| `blockchain_client` | `8081` (default) | Wallet UI: key generation, transaction signing |

A second node (`blockchain-node-2`) is declared in `docker-compose.yml` on port `5002` to facilitate P2P consensus testing locally.

---

## 📁 Project Structure

```
pow-blockchain-python/
├── blockchain/                     # Blockchain Node service
│   ├── api/
│   │   └── routes.py               # FastAPI endpoints (chain, mine, transactions, nodes)
│   ├── application/
│   │   └── services.py             # BlockchainService: mine, submit_tx, resolve_conflicts
│   ├── domain/
│   │   ├── entities.py             # Block & Transaction dataclasses with to_dict()
│   │   └── logic.py                # BlockchainLogic: SHA-256 hashing, valid_proof, proof_of_work
│   ├── infrastructure/
│   │   ├── crypto.py               # RSA signature verification (PyCryptodome)
│   │   └── p2p.py                  # P2PClient: register_node, fetch_chain
│   ├── templates/                  # Jinja2 HTML templates
│   ├── static/                     # JS/CSS assets
│   └── main.py                     # App factory, DI wiring, uvicorn entrypoint
│
├── blockchain_client/              # Wallet Client service
│   ├── api/
│   │   └── routes.py               # Wallet endpoints (new wallet, generate/sign tx)
│   ├── application/
│   │   └── wallet_service.py       # WalletService: create_wallet, create_and_sign_transaction
│   ├── domain/
│   │   └── transaction.py          # Transaction domain model (client-side)
│   ├── infrastructure/
│   │   └── crypto.py               # RSA key generation & signing (PyCryptodome)
│   ├── templates/                  # Jinja2 HTML templates
│   ├── static/                     # JS/CSS assets
│   └── main.py                     # App factory, DI wiring, uvicorn entrypoint
│
├── tests/
│   ├── conftest.py                 # Shared pytest fixtures (TestClient for both apps)
│   ├── blockchain/
│   │   ├── unit/
│   │   │   ├── test_entities.py    # Block & Transaction dataclass tests
│   │   │   ├── test_domain_logic.py# Hash, valid_proof, proof_of_work tests
│   │   │   └── test_infrastructure.py # CryptoService, P2PClient unit tests
│   │   ├── integration/
│   │   │   └── test_api_routes.py  # HTTP endpoint integration tests
│   │   └── feature/
│   │       └── test_mining_flow.py # Full end-to-end mining scenario
│   └── blockchain_client/
│       ├── unit/                   # Wallet & crypto unit tests
│       └── integration/            # Client endpoint integration tests
│
├── Dockerfile                      # Python 3.12-slim image definition
├── docker-compose.yml              # Node 1 (5001) + Node 2 (5002) + Client (8081)
├── Makefile                        # Developer shortcuts (build, up, test, lint, format)
├── pyproject.toml                  # Black & tooling config
├── requirements.txt                # All Python dependencies (pinned)
├── .env.example                    # Environment variable template
└── .flake8                         # Flake8 linting config
```

---

## ⚙️ Configuration

Copy the example file before running:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | Environment tag (`development` / `production`) |
| `BLOCKCHAIN_HOST` | `0.0.0.0` | Blockchain node bind host |
| `BLOCKCHAIN_PORT` | `5001` | Blockchain node port |
| `BLOCKCHAIN_CLIENT_HOST` | `0.0.0.0` | Wallet client bind host |
| `BLOCKCHAIN_CLIENT_PORT` | `8081` | Wallet client port |
| `MINING_DIFFICULTY` | `2` | PoW difficulty (leading zeros required in hash) |
| `MINING_REWARD` | `1` | Coinbase reward per mined block |
| `MINING_SENDER` | `"The Blockchain"` | Pseudo-identity for coinbase transactions |
| `PYTHONPATH` | `.` | Ensures local package imports resolve correctly |

> **Tip:** Increase `MINING_DIFFICULTY` to simulate realistic mining latency. A value of `4` is already slow on a laptop; Bitcoin uses 19+.

---

## 🚀 How to Run

### Makefile targets (Docker-based)

```bash
make help       # List all available targets

make build      # Build Docker images
make up         # Start all services in the background (docker compose up -d)
make down       # Stop and remove containers
make restart    # down + up in one step
make clean      # Remove __pycache__, *.pyc, .pytest_cache, .venv
```

After `make up`, services are available at:
- **Node 1 (UI + API):** http://localhost:5001
- **Node 2 (P2P peer):** http://localhost:5002
- **Wallet Client (UI + API):** http://localhost:8081

### Local Virtual Environment (no Docker)

```bash
# 1. Create and activate venv
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment config
cp .env.example .env

# 4. Run each service in a separate terminal

# Terminal 1 — Blockchain Node 1
python blockchain/main.py -p 5001

# Terminal 2 — Blockchain Node 2 (optional, for P2P)
python blockchain/main.py -p 5002

# Terminal 3 — Wallet Client
python blockchain_client/main.py -p 8081
```

---

## 📡 API Reference

### Blockchain Node (`http://localhost:5001`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web UI — mining dashboard |
| `GET` | `/configure` | Web UI — P2P node registration |
| `GET` | `/chain` | Returns full blockchain (`chain`, `length`) |
| `GET` | `/mine` | Executes PoW and appends a new block |
| `GET` | `/transactions/get` | Lists all pending mempool transactions |
| `POST` | `/transactions/new` | Submits a signed transaction to the mempool |
| `GET` | `/nodes/get` | Lists all registered peer nodes |
| `POST` | `/nodes/register` | Registers one or more peer nodes |
| `GET` | `/nodes/resolve` | Runs Nakamoto consensus (longest valid chain wins) |

**POST `/transactions/new` form fields:**

```
confirmation_sender_public_key   (hex-encoded RSA public key)
confirmation_recipient_public_key(hex-encoded RSA public key)
transaction_signature            (hex-encoded RSA signature)
confirmation_amount              (float)
```

### Blockchain Client / Wallet (`http://localhost:8081`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web UI — wallet home |
| `GET` | `/wallet/new` | Generates a new RSA key pair (public + private key, hex-encoded) |
| `GET` | `/make/transaction` | Web UI — transaction signing form |
| `GET` | `/view/transactions` | Web UI — live mempool viewer |
| `POST` | `/generate/transaction` | Creates and RSA-signs a transaction, returns `{transaction, signature}` |

---

## 🧪 How to Test

### Makefile targets (Docker-based)

```bash
make test       # Run full test suite inside the blockchain-node container
                # → docker compose run --rm blockchain-node pytest tests/

make lint       # Enforce code style inside Docker
                # → flake8 . && black --check .

make format     # Auto-format code inside Docker
                # → black .
```

### Run Tests Locally (no Docker)

```bash
# Activate venv first
source .venv/bin/activate

# All tests
pytest tests/

# Specific test layers
pytest tests/blockchain/unit/
pytest tests/blockchain/integration/
pytest tests/blockchain/feature/
pytest tests/blockchain_client/

# Verbose output + short tracebacks
pytest tests/ -v --tb=short

# Stop on first failure
pytest tests/ -x

# Lint & format locally
flake8 .
black blockchain blockchain_client tests
```

### Test Matrix

| Test Type | Location | What it covers |
|---|---|---|
| **Unit — Entities** | `tests/blockchain/unit/test_entities.py` | `Block.to_dict()`, `Transaction.to_dict()`, field presence |
| **Unit — Logic** | `tests/blockchain/unit/test_domain_logic.py` | `hash_block` determinism, `valid_proof`, `proof_of_work` round-trip |
| **Unit — Infrastructure** | `tests/blockchain/unit/test_infrastructure.py` | `CryptoService.verify_signature`, `P2PClient.register_node` |
| **Integration — API** | `tests/blockchain/integration/test_api_routes.py` | `/chain`, `/mine`, `/transactions/new`, `/nodes/register` via `TestClient` |
| **Feature — Mining Flow** | `tests/blockchain/feature/test_mining_flow.py` | Full E2E: wallet → sign → submit → mine → verify chain |
| **Client — Unit** | `tests/blockchain_client/unit/` | `WalletService`, client-side `CryptoService` |
| **Client — Integration** | `tests/blockchain_client/integration/` | `/wallet/new`, `/generate/transaction` endpoints |

---

## 🔄 Test Flow (E2E Walkthrough)

This describes the full lifecycle of a transaction from wallet creation to block confirmation, as covered by `test_mining_flow.py`:

```
Step 1 — Generate Wallet
  GET /wallet/new  →  { public_key: "...", private_key: "..." }

Step 2 — Sign Transaction
  POST /generate/transaction
  Body: { sender_public_key, sender_private_key, recipient_public_key, amount }
  →  { transaction: { sender_public_key, recipient_public_key, amount }, signature: "..." }

Step 3 — Submit to Mempool
  POST /transactions/new (on blockchain node port 5001)
  Body: { confirmation_sender_public_key, confirmation_recipient_public_key,
          transaction_signature, confirmation_amount }
  →  HTTP 201 + "Transaction will be added to Block N"

Step 4 — Verify Mempool
  GET /transactions/get
  →  { transactions: [ { sender_public_key, recipient_public_key, amount } ] }
  Assert: len == 1

Step 5 — Mine Block
  GET /mine
  →  { message: "New block created", block_number, timestamp, transactions, nonce, previous_hash }
  Assert: HTTP 200

Step 6 — Verify Chain
  GET /chain
  →  { chain: [...], length: 2 }
  Assert: chain[1].transactions has 2 entries (1 user tx + 1 coinbase reward)
```

**Manual walkthrough via browser:**

1. Open **Wallet Client** → `http://localhost:8081` → click **Generate Wallet**, save both keys.
2. Go to **Make Transaction** → fill in sender keys, a recipient public key (can be any hex string for demo), and an amount → click **Generate Transaction**.
3. Copy the generated transaction + signature; submit it to the node via the form (pointing to `http://localhost:5001`).
4. Open **Node 1** → `http://localhost:5001` → click **Mine**.
5. Refresh the chain view and confirm the new block with 2 transactions (yours + coinbase).
6. *(Optional P2P)* Open **Node 2** (`http://localhost:5002`) → Configure → register `http://localhost:5001` → click **Resolve Conflicts** — Node 2 replaces its chain with Node 1's longer one.

---

## 📋 TODO — Production Readiness

### Phase 1 — Persistence & Reliability

- [ ] **Persistent storage**: Replace in-memory `self.chain` and `self.transactions` lists with a durable store (RocksDB, LevelDB, or PostgreSQL via SQLAlchemy — dependency already in `requirements.txt`). Nodes currently lose all data on restart.
- [ ] **Write-Ahead Log (WAL)**: Journal every transaction and block append before committing to state, enabling crash recovery.
- [ ] **Structured logging**: Replace `print`-style debugging with a structured logger (e.g., `structlog`) with log levels, request IDs, and JSON output for log aggregation.
- [ ] **Observability**: Expose Prometheus metrics (block height, pending tx count, hash rate, mine duration) for Grafana dashboards.
- [ ] **Health check endpoint**: Add `GET /health` returning service status, chain length, and peer count — required for Docker/k8s readiness probes.

### Phase 2 — Cryptography & Security

- [ ] **Upgrade hash function**: The signature verification currently uses `SHA` (SHA-1). **Migrate to SHA-256** (`from Crypto.Hash import SHA256`) to align with modern standards.
- [ ] **Secure node communication**: All inter-node HTTP is currently plaintext. Wrap with TLS and implement shared-secret or certificate-based authentication for `/nodes/register` and `/nodes/resolve`.
- [ ] **Rate limiting**: The `/mine` and `/transactions/new` endpoints have no rate limiting, making them trivially DoS-able. Add `slowapi` or an nginx upstream rate limiter.
- [ ] **Private key never leaves client**: Currently the private key is submitted as a form field to `POST /generate/transaction`. Signing should happen client-side (WebCrypto API or a local CLI) — the server should never see the private key.
- [ ] **HD Wallets (BIP-32/39/44)**: Replace one-shot RSA keypairs with hierarchical deterministic wallets for proper key derivation and seed phrase recovery.
- [ ] **Restrict CORS**: `blockchain/main.py` currently sets `allow_origins=["*"]`. Restrict to known frontend origins in production.

### Phase 3 — Networking & Consensus

- [ ] **Push-based broadcasting**: The current consensus is pull-only (`/nodes/resolve`) — nodes never learn about new blocks until manually asked. Implement WebSocket or webhook broadcasting so new blocks and transactions propagate instantly.
- [ ] **Peer discovery (Gossip protocol)**: Nodes must currently be registered manually. Implement a gossip-based discovery protocol so nodes find each other via an initial seed list.
- [ ] **Fork resolution robustness**: The `resolve_conflicts` implementation assumes it can poll all nodes synchronously over HTTP. In practice this will time out; replace with an async background task.
- [ ] **Node identity & persistence**: The `node_id` (UUID) is regenerated on every restart. Persist it so peers can consistently identify the same node.

### Phase 4 — Mining & Protocol

- [ ] **Async mining**: `GET /mine` blocks the entire event loop during PoW computation. Move mining to a `asyncio` executor or a background `multiprocessing` worker, returning a job ID that can be polled.
- [ ] **Difficulty retargeting**: `MINING_DIFFICULTY` is a static env var. Implement dynamic difficulty adjustment (similar to Bitcoin's 2-week retarget) based on average block time over the last N blocks.
- [ ] **Merkle Trees**: Block transactions are hashed as a flat list. Replace with a Merkle tree to enable efficient SPV proofs and partial transaction verification without downloading the full block.
- [ ] **Transaction fees & mempool priority**: There is no fee mechanism. Add a `fee` field to `Transaction`, and prioritize high-fee transactions for inclusion in the next block.
- [ ] **Double-spend prevention**: The node has no UTXO set or balance ledger. A sender can submit the same signed transaction multiple times and both will be accepted into the mempool.
- [ ] **Mempool eviction**: Unconfirmed transactions accumulate indefinitely. Add TTL and size limits with eviction policies.
- [ ] **Genesis block standardisation**: The genesis block is created with `nonce=0` and `previous_hash="00"` — these are hardcoded magic values. Define them as named constants or config.

### Phase 5 — Scalability & DevOps

- [ ] **Test coverage gates**: No coverage thresholds are enforced. Add `pytest-cov` and a CI rule that fails below 80% coverage.
- [ ] **Continuous Integration**: Add a GitHub Actions workflow to run `make lint` and `make test` on every PR.
- [ ] **Multi-stage Dockerfile**: The current Dockerfile installs all dev dependencies (flake8, black, pytest) into the production image. Use a multi-stage build to produce a lean runtime image.
- [ ] **Secrets management**: `.env` is handled via `python-dotenv`. In a cloud deployment, replace with a proper secrets manager (AWS Secrets Manager, HashiCorp Vault), and ensure `.env` is never committed.
- [ ] **OpenAPI documentation**: FastAPI auto-generates `/docs` (Swagger UI) and `/redoc`. Add `summary`, `description`, `response_model`, and `tags` to all route handlers to produce meaningful API documentation.
- [ ] **Remove unused dependencies**: `psycopg2-binary`, `SQLAlchemy`, `greenlet`, and `pytokens` are listed in `requirements.txt` but are not used anywhere in the codebase.

---

## 🐛 Known Bugs & Required Fixes

### Critical

| # | Location | Bug | Fix |
|---|---|---|---|
| 1 | `blockchain/infrastructure/crypto.py` | Uses `SHA` (SHA-1) for signature verification — SHA-1 is cryptographically broken | Replace `from Crypto.Hash import SHA` with `from Crypto.Hash import SHA256` and update all hash usages |
| 2 | `blockchain/application/services.py` | `resolve_conflicts` calls `self.p2p_client.fetch_chain(node)` synchronously inside an async endpoint — blocks the uvicorn event loop for all peers | Wrap with `asyncio.get_event_loop().run_in_executor(None, ...)` or use `httpx.AsyncClient` |
| 3 | `blockchain_client/api/routes.py` | The `sender_private_key` is transmitted in plaintext over HTTP to the server for signing | Signing must move to the client side; the server should only receive the public key, transaction, and signature |

### High

| # | Location | Bug | Fix |
|---|---|---|---|
| 4 | `blockchain/application/services.py` | No double-spend check: the same signed transaction can be submitted multiple times to the mempool | Track transaction hashes in a set; reject previously-seen transactions |
| 5 | `blockchain/application/services.py` | `_valid_chain` silently skips validation of coinbase (mining reward) transactions by slicing `[:-1]` — a malicious node could insert a fake reward transaction | Validate all transactions or explicitly tag and verify coinbase transactions separately |
| 6 | `blockchain/infrastructure/p2p.py` | `register_node` accepts bare paths (e.g. `127.0.0.1:5002`) but loses the scheme — `netloc` will be empty for bare host:port strings if no scheme is provided | Normalise input by prepending `http://` if no scheme is present before parsing |
| 7 | `blockchain/api/routes.py` | `GET /mine` is a side-effect endpoint; it modifies state (appends a block) over a GET request, violating HTTP semantics and breaking caching | Change to `POST /mine` |

### Medium

| # | Location | Bug | Fix |
|---|---|---|---|
| 8 | `blockchain/application/services.py` | `MINING_SENDER`, `MINING_REWARD`, `MINING_DIFFICULTY` are module-level constants read once at import time — changing `.env` at runtime has no effect | Move them into `BlockchainService.__init__` or read them via a config object |
| 9 | `blockchain/domain/entities.py` | `Transaction.to_dict()` silently omits the `signature` field — downstream code in `_valid_chain` reconstructs an `OrderedDict` from a hardcoded list of keys, making it fragile to field additions | Add an explicit `include_signature: bool = False` parameter to `to_dict()` |
| 10 | `blockchain/application/services.py` | `mine()` calls `submit_transaction()` to add the coinbase reward but this re-runs the signature verification path (guarded by `if sender_public_key == MINING_SENDER`) — a string comparison is the only "auth" for creating money | Mark coinbase transactions with an explicit type flag instead of relying on a magic sender string |
| 11 | `tests/blockchain/unit/test_domain_logic.py` | `test_valid_proof` computes a nonce manually inside the test and then finds a second valid nonce via `proof_of_work` in the same assertion block — the `nonce` binding from `proof_of_work` is immediately overwritten, making the first assertion dead code | Rewrite to cleanly separate the two sub-cases |

### Low / Cosmetic

| # | Location | Bug | Fix |
|---|---|---|---|
| 12 | `requirements.txt` | `black==26.1.0` — this version does not exist as of writing; likely a placeholder or typo | Pin to the latest stable release (e.g. `black==24.4.2`) |
| 13 | `docker-compose.yml` | No `depends_on` or health checks — `blockchain-client` may start before any node is ready | Add `depends_on: blockchain-node` with a health check condition |
| 14 | `Dockerfile` | No `ENTRYPOINT` or `CMD` — the container has no default command; the only way to run it is via `docker compose` with an explicit `command:` override | Add a sensible default `CMD` |
| 15 | `blockchain/main.py` | `allow_credentials=True` with `allow_origins=["*"]` is rejected by browsers (CORS spec forbids wildcard + credentials) | Either remove `allow_credentials=True` or use an explicit allowed-origins list |

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
