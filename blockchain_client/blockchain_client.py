from flask import Flask, render_template

class Transaction:
    def __init__(
            self,
            sender_address,
            sender_private_key,
            receiver_address,
            value
    ):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.receiver_address = receiver_address
        self.value = value


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/make/transaction")
def make_transaction():
    return render_template("make_transaction.html")


@app.route("/view/transaction")
def view_transaction():
    return render_template("view_transaction.html")


@app.route("/wallet/new")
def new_wallet():
    return ""


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8081, help="Port to listen on")
    args = parser.parse_args()
    port = args.port
    app.run(host="127.0.0.1", port=port, debug=True)