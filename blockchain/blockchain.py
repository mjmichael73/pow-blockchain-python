from flask import Flask, request, jsonify, render_template
from time import time
from flask_cors import CORS
from collections import OrderedDict
import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from uuid import uuid4

MINING_SENDER = "The Blockchain"
MINING_REWARD = 1


class Blockchain:

    def __init__(self):
        self.transactions = []
        self.chain = []
        self.node_id = str(uuid4()).replace("-", "")
        # Create the genesis block
        self.create_block(0, "00")

    def create_block(self, nonce, previous_hash):
        """
        Add a block of transactions to the blockchain
        """
        block = {
            "block_number": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.transactions,
            "nonce": nonce,
            "previous_hash": previous_hash,
        }

        # Reset the current list of transactions
        self.transactions = []
        self.chain.append(block)
        return block

    def verify_transaction_signature(self, sender_public_key, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode("utf8"))
        try:
            verifier.verify(h, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False

    def proof_of_work(self):
        return 12345

    def hash(self, block):
        return "abc"

    def submit_transaction(
        self, sender_public_key, recipient_public_key, signature, amount
    ):
        transaction = OrderedDict(
            {
                "sender_public_key": sender_public_key,
                "recipient_public_key": recipient_public_key,
                "amount": amount,
            }
        )

        # Reward for mining a block
        if sender_public_key == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        else:
            # Transaction from wallet to another wallet
            signature_verification = self.verify_transaction_signature(
                sender_public_key, signature, transaction
            )
            if signature_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
            else:
                return False


# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate the Node
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("./index.html")


@app.route("/transactions/get", methods=["GET"])
def get_transactions():
    transactions = blockchain.transactions
    response = {"transactions": transactions}
    return jsonify(response), 200


@app.route("/chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}

    return jsonify(response), 200


@app.route("/mine", methods=["GET"])
def mine():
    # We run the proof of work algorithm
    nonce = blockchain.proof_of_work()

    blockchain.submit_transaction(
        sender_public_key=MINING_SENDER,
        recipient_public_key=blockchain.node_id,
        signature="",
        amount=MINING_REWARD,
    )

    last_block = blockchain.chain[-1]
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)

    response = {
        "message": "New block created",
        "block_number": block["block_number"],
        "transactions": block["transactions"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.form
    required = [
        "confirmation_sender_public_key",
        "confirmation_recipient_public_key",
        "transaction_signature",
        "confirmation_amount",
    ]
    if not all(k in values for k in required):
        return "Missing values", 400

    transaction_results = blockchain.submit_transaction(
        values["confirmation_sender_public_key"],
        values["confirmation_recipient_public_key"],
        values["transaction_signature"],
        values["confirmation_amount"],
    )
    if transaction_results is False:
        response = {"message": "Invalid transaction/signature"}
        return jsonify(response), 406
    else:
        response = {
            "message": "Transaction will be added to the Block "
            + str(transaction_results)
        }
        return jsonify(response), 201


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5001, type=int, help="port to listen to"
    )
    args = parser.parse_args()
    port = args.port

    app.run(host="127.0.0.1", port=port, debug=True)
