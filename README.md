# 🧙‍♂️ Polkadot XCM Wizard v8.0

> **"Build Once, Bridge Everywhere."**
> Satu-satunya alat infrastruktur berbasis CLI dan Web dApp untuk membangun Smart Contract Cross-Consensus Messaging (XCM) yang aman di Polkadot Hub & Parachains.

![Polkadot](https://img.shields.io/badge/Polkadot-E6007A?style=for-the-badge&logo=polkadot&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Solidity](https://img.shields.io/badge/Solidity-363636?style=for-the-badge&logo=solidity&logoColor=white)

---

## 🚀 Apa itu Polkadot XCM Wizard?
Menulis pesan XCM secara manual sangatlah rumit dan berisiko tinggi (dana bisa terkunci selamanya). **XCM Wizard v8.0** hadir untuk mengotomatiskan proses ini. 

Sekarang tersedia dalam dua versi:
1.  **Web dApp (Streamlit):** Interface modern bagi pengguna yang ingin kemudahan klik-dan-generate.
2.  **CLI Tool:** Untuk developer hardcore yang bekerja melalui terminal.

## ✨ Fitur Unggulan v8.0
* **Universal Bridge:** Mendukung transfer Native Token (GLMR/ASTR/DOT) dan ERC-20 dalam satu contract.
* **Auto-Refund Logic:** Dana otomatis kembali ke pengirim jika eksekusi XCM gagal.
* **Multi-Format Encoding:** Mendukung AccountKey20 (Ethereum-style) dan AccountId32 (Substrate-style).
* **Security First:** Dilengkapi dengan ReentrancyGuard dan OpenZeppelin SafeERC20.

---

## 🛠️ Cara Instalasi & Penggunaan

### 1. Persiapan
Pastikan Python sudah terinstal di komputer Anda. Kemudian instal library yang dibutuhkan:
```bash
pip install streamlit
