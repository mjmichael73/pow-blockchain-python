from time import time
from flask import Flask, render_template


class Blockchain:
    def __init__(self):
        self.transactions = []
        self.chain = []
        # Create the genesis block
        self.create_block(
            nonce=0,
            previous_hash="00",
        )

    def create_block(self, nonce, previous_hash):
        """
        Add a block of transaction to the blockchain
        :param nonce:
        :param previous_hash:
        :return:
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

        # Add the new block to the chain
        self.chain.append(block)


# Instantiate the Blockchain
blockchain = Blockchain()


# Instantiate the Node
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("./index.html")


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5001, help="Port to listen on")
    args = parser.parse_args()
    port = args.port
    app.run(host="127.0.0.1", port=port, debug=True)

