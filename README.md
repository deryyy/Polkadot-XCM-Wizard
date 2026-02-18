# 🧙‍♂️ Polkadot XCM Wizard v8.0

> **"Build Once, Bridge Everywhere."**
> The ultimate infrastructure tool to automate secure Cross-Consensus Messaging (XCM) smart contracts for Polkadot Hub & Parachains.

![Polkadot](https://img.shields.io/badge/Polkadot-E6007A?style=for-the-badge&logo=polkadot&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Solidity](https://img.shields.io/badge/Solidity-363636?style=for-the-badge&logo=solidity&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 🚀 Overview
Writing raw XCM messages is complex, error-prone, and carries high risks (e.g., permanently locked funds). **Polkadot XCM Wizard v8.0** solves this by providing a developer-friendly interface to generate production-ready Solidity bridge contracts in seconds.

Whether you are a CLI power user or prefer a modern Web UI, we’ve got you covered.

## ✨ Key Features (v8.0)
* **Universal Bridge:** A single contract for both Native Assets (GLMR, ASTR, DOT) and ERC-20 tokens.
* **Production-Ready Security:** Integrated with OpenZeppelin’s `Ownable`, `ReentrancyGuard`, and `SafeERC20`.
* **Auto-Refund Logic:** Automatically returns funds to the sender if the XCM execution fails at the destination.
* **Smart Multi-Location Encoding:** Seamlessly handles **AccountKey20** (Ethereum-style) and **AccountId32** (Substrate-style) formats.
* **XCM v3 Optimized:** Pre-configured with efficient `WithdrawAsset` -> `BuyExecution` -> `DepositAsset` instruction sets.

---

## 🛠️ Installation & Usage

### 1. Prerequisites
Ensure you have Python installed. Install the required dependencies:
```bash
pip install streamlit
