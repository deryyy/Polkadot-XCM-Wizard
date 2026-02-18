# 🧙‍♂️ Polkadot XCM Wizard (CLI Tool)

> **"Build Once, Bridge Everywhere."**
> The ultimate infrastructure CLI tool to scaffold secure Cross-Consensus Messaging (XCM) smart contracts for Polkadot Hub & Parachains.

![Polkadot Badge](https://img.shields.io/badge/Polkadot-E6007A?style=for-the-badge&logo=polkadot&logoColor=white)
![Python Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Solidity Badge](https://img.shields.io/badge/Solidity-363636?style=for-the-badge&logo=solidity&logoColor=white)
![License Badge](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🚨 The Problem
Writing raw XCM messages manually is a nightmare for developers:
1.  **Complexity**: Constructing `MultiLocation` and byte-encoding `WithdrawAsset` -> `BuyExecution` -> `DepositAsset` is error-prone.
2.  **Risk**: One wrong byte calculation can lead to **permanently locked funds**.
3.  **Fragmented Standards**: Different Parachains use different account formats (20-byte Ethereum vs 32-byte Substrate).

## 🛠️ The Solution
**XCM Wizard v8.0** automates the entire engineering process. In **< 1 second**, it generates a **Universal Bridge Smart Contract** that is:
* **Production-Ready**: Pre-configured with OpenZeppelin security modules.
* **Universal**: One contract handles **BOTH** Native (GLMR/ASTR/DOT) and ERC-20 token transfers.
* **Fault-Tolerant**: Built-in `auto-refund` logic if XCM execution fails.

---

## ✨ Key Features (v8.0)

### 🛡️ Universal Architecture
No need to deploy separate contracts. The generated code includes:
- `bridgeNative()`: For bridging gas tokens (e.g., GLMR, MOVR).
- `bridgeERC20()`: For bridging any standard ERC-20 token (e.g., USDT, USDC).

### 🤖 Smart Encoding & Validation
- **Input Validation**: The CLI prevents crashes by validating Parach
