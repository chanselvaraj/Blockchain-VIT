from flask import Flask, request, jsonify,render_template
from blockchain import Blockchain

app = Flask(__name__)

# Initialize blockchain
bc = Blockchain(difficulty=3, coinbase_amount=50)

# ------------------------
# Wallet endpoints
# ------------------------

@app.route("/wallet/create", methods=["POST"])
def create_wallet():
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "Provide wallet name"}), 400
    wallet = bc.create_wallet(name)
    return jsonify(wallet)

@app.route("/wallets")
def list_wallets():
    return jsonify({k: w.to_dict() for k, w in bc.wallets.items()})

@app.route("/balance/<address>")
def balance(address):
    bal = bc.get_balance(address)
    return jsonify({"address": address, "balance": bal})

# ------------------------
# Transaction endpoints
# ------------------------

@app.route("/tx/new", methods=["POST"])
def new_tx():
    data = request.json
    sender = data["from"]
    receiver = data["to"]
    amount = int(data["amount"])
    try:
        tx = bc.create_transaction(sender, receiver, amount)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(tx)

@app.route("/mempool")
def mempool():
    return jsonify([tx.to_dict() for tx in bc.mempool])

# ------------------------
# Mining endpoint
# ------------------------

@app.route("/mine", methods=["POST"])
def mine():
    miner = request.json.get("miner")
    block = bc.mine_block(miner_address=miner)
    return jsonify(block)

# ------------------------
# Blockchain
# ------------------------

@app.route("/chain")
def chain():
    return jsonify(bc.to_dict())

@app.route("/")
def home():
    return render_template("dashboard.html")
    # return jsonify({"message": "Simplified Bitcoin Blockchain API running"})

# ------------------------
# Run server
# ------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
