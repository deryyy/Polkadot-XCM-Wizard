# ????? Polkadot XCM Wizard (CLI)

> **"Build Once, Scale Everywhere."**
> The automated infrastructure tool to scaffold Cross-Consensus Messaging (XCM) smart contracts for Polkadot Hub.

![Polkadot Badge](https://img.shields.io/badge/Polkadot-E6007A?style=for-the-badge&logo=polkadot&logoColor=white)
![Python Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Solidity Badge](https://img.shields.io/badge/Solidity-363636?style=for-the-badge&logo=solidity&logoColor=white)
![License Badge](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ?? The Problem
Developing on **Polkadot Hub** allows access to the entire ecosystem, but writing **raw XCM messages** (calculating bytes for `WithdrawAsset`, `BuyExecution`, `DepositAsset`) is:
1.  **Complex**: Requires deep knowledge of MultiLocation standards.
2.  **Error-Prone**: One wrong byte calculation leads to lost assets.
3.  **Time-Consuming**: Developers waste hours debugging hex codes.

## ??? The Solution
**XCM Wizard** is a Python-based CLI tool that automates this process. It generates production-ready, secure Solidity smart contracts pre-configured to bridge assets to any Parachain (Moonbeam, Acala, Astar, etc).

### ? Key Features
- **?? Automated Byte-Encoding**: Automatically calculates `abi.encodePacked` for low-level XCM instructions.
- **? Polkadot-Native**: Optimized for Polkadot Hub EVM Precompiles (`0x00...0804`).
- **??? Secure Scaffolding**: Includes `ReentrancyGuard` and `Ownable` by default.
- **wizard Interactive Interface**: A clean, professional CLI wizard for rapid development.

---

## ?? Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/deryyy/Polkadot-XCM-Wizard.git](https://github.com/deryyy/Polkadot-XCM-Wizard.git)
cd Polkadot-XCM-Wizard