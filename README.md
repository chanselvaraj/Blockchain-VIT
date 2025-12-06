# **VIT Demo: Simplified Blockchain Implementation**

A **Python-based mini Bitcoin-like blockchain** project demonstrating key blockchain concepts including **wallets, transactions, UTXOs, mining, proof-of-work, and a P2P network**, with a **browser-based dashboard** for visualization.

---

## **Project Overview**

This project implements a **simplified Bitcoin-like blockchain** in Python for educational purposes.  

Key aspects demonstrated:

- Transaction creation & verification using **ECDSA signatures**  
- **UTXO-based accounting** (unspent transaction outputs)  
- **Block creation & Proof-of-Work mining**  
- Simple **P2P networking** with broadcasting transactions and blocks  
- **Flask-based API** and **browser dashboard** for visualization  

---

## **Features**

- **Wallets & Addresses**: Generate ECDSA keypairs and addresses for users.  
- **Transactions**: Send coins between wallets with digital signature verification.  
- **UTXO Management**: Track unspent outputs for validation and balance calculation.  
- **Mining**: Mine blocks with configurable reward and difficulty.  
- **Blockchain**: Blocks linked with hashes, Proof-of-Work, and transaction validation.  
- **P2P Network**: Broadcast transactions and blocks to peers, synchronize chains.  
- **Dashboard**: Web interface to view wallets, balances, mempool, blockchain, and mine blocks.  

---

## **Architecture & Components**
- MiniBitcoin/
- │
- ├─ blockchain.py # Core blockchain logic
- │ ├─ Wallet # ECDSA keypair generation, signing, verification
- │ ├─ Transaction # Inputs, outputs, signing, verification
- │ ├─ UTXOSet # Unspent Transaction Output management
- │ ├─ Mempool # Pending transactions
- │ ├─ Block # Block structure and hash calculation
- │ ├─ Blockchain # Chain, validation, genesis block
- │ └─ Miner # Mining functionality
- │
- ├─ api.py # Flask API for interaction with blockchain
- │
- ├─ templates/
- │ └─ dashboard.html # Browser-based dashboard UI
- │
- ├─ static/ # Optional: CSS, JS files for frontend
- │
- └─ README.md

--
## **Getting Started**

### **Requirements**

- Python 3.8+
- pip packages:


## **Running the Project**

- Start the Flask API server:
```bash
 python api.py
```

- Open the dashboard in your browser:
```bash
- http://127.0.0.1:5000/
```
