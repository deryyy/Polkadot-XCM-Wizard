#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
import textwrap
import re
from datetime import datetime

class Style:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    @staticmethod
    def print_step(step, msg):
        print(f"{Style.GREEN}[{step}]{Style.RESET} {msg}")

class SolidityTemplates:
    @staticmethod
    def get_xcm_contract(p_name, author, para_id, acc_format, xcm_pre, p_idx, weight):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Target account encoding
        if acc_format == "ethereum":
            acc_enc = "uint8(1), uint8(0), beneficiaryBytes"
            len_check = "beneficiaryBytes.length == 20"
        else:
            acc_enc = "uint8(0), uint8(0), beneficiaryBytes"
            len_check = "beneficiaryBytes.length == 32"

        return textwrap.dedent(f"""\
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.20;

            import "@openzeppelin/contracts/access/Ownable.sol";
            import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
            import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
            import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

            /**
             * @title  {p_name} Universal Bridge
             * @author {author}
             * @notice Generated on {timestamp} for Polkadot Solidity Hackathon
             * @dev XCM v3 with WithdrawAsset -> BuyExecution (Limited) -> DepositAsset (Wild All)
             */
            contract {p_name.replace(" ", "")}Bridge is Ownable, ReentrancyGuard {{
                using SafeERC20 for IERC20;

                // --- CONFIGURATION ---
                uint32 public constant DESTINATION_PARA_ID = {para_id};
                address public immutable XCM_PRECOMPILE;
                uint64 public defaultWeight = {weight};
                uint8 public palletIndex = {p_idx};

                // --- EVENTS ---
                event XcmSent(address indexed sender, bytes32 indexed beneficiaryHash, uint256 amount, bytes32 indexed xcmHash);
                event XcmFailed(bytes32 indexed xcmHash, bytes reason);

                constructor(address _xcmPrecompile) Ownable(msg.sender) {{
                    XCM_PRECOMPILE = _xcmPrecompile;
                }}

                // ==========================================
                //              NATIVE BRIDGE
                // ==========================================

                function bridgeNative(address beneficiary, uint128 amount) external payable {{
                    bridgeNative(abi.encodePacked(beneficiary), amount);
                }}

                function bridgeNative(bytes memory beneficiaryBytes, uint128 amount) public payable nonReentrant {{
                    require(msg.value >= amount, "Insufficient payment");
                    require({len_check}, "Invalid beneficiary length");

                    // Destination: parents=1, interior=X2(ParaId, Account)
                    bytes memory dest = abi.encodePacked(
                        uint8(1), uint8(2), uint8(0), uint32(DESTINATION_PARA_ID), {acc_enc}
                    );

                    // Message: WithdrawAsset (3) -> BuyExecution (4) -> DepositAsset (6)
                    // WithdrawAsset: 1 asset, Here (0x00), amount
                    // BuyExecution: Limited (1), weight
                    // DepositAsset: Wild All (0), beneficiary
                    bytes memory message = abi.encodePacked(
                        uint8(3),                        // WithdrawAsset
                        uint8(1),                        // assets count = 1
                        uint8(0),                        // Here (native)
                        amount,                          // amount (uint128)
                        uint8(4),                        // BuyExecution
                        uint8(1),                        // Limited
                        uint64(defaultWeight),           // weight
                        uint8(6),                        // DepositAsset
                        uint8(0),                        // Wild All
                        beneficiaryBytes                 // beneficiary
                    );

                    (bool success, bytes memory returnData) = XCM_PRECOMPILE.call(
                        abi.encodeWithSignature("xcmSend(bytes,bytes)", dest, message)
                    );
                    bytes32 xcmHash = keccak256(message);

                    if (!success) {{
                        emit XcmFailed(xcmHash, returnData);
                        payable(msg.sender).transfer(amount);
                    }} else {{
                        emit XcmSent(msg.sender, keccak256(beneficiaryBytes), amount, xcmHash);
                    }}
                }}

                // ==========================================
                //              ERC-20 BRIDGE
                // ==========================================

                function bridgeERC20(address tokenAddress, address beneficiary, uint128 amount) external nonReentrant {{
                    bridgeERC20(tokenAddress, abi.encodePacked(beneficiary), amount);
                }}

                function bridgeERC20(address tokenAddress, bytes memory beneficiaryBytes, uint128 amount) public nonReentrant {{
                    require({len_check}, "Invalid beneficiary length");
                    IERC20(tokenAddress).safeTransferFrom(msg.sender, address(this), amount);

                    bytes memory dest = abi.encodePacked(
                        uint8(1), uint8(2), uint8(0), uint32(DESTINATION_PARA_ID), {acc_enc}
                    );

                    // Asset location: parents=1, interior=X2(PalletInstance(palletIndex), GeneralIndex(tokenAddress))
                    bytes memory assetLocation = abi.encodePacked(
                        uint8(1), uint8(2), uint8(3), uint8(palletIndex), uint8(0), uint128(uint160(tokenAddress))
                    );

                    bytes memory message = abi.encodePacked(
                        uint8(3),                        // WithdrawAsset
                        uint8(1),                        // assets count = 1
                        assetLocation,                   // asset location
                        amount,                          // amount
                        uint8(4),                        // BuyExecution
                        uint8(1),                        // Limited
                        uint64(defaultWeight),           // weight
                        uint8(6),                        // DepositAsset
                        uint8(0),                        // Wild All
                        beneficiaryBytes                 // beneficiary
                    );

                    (bool success, bytes memory returnData) = XCM_PRECOMPILE.call(
                        abi.encodeWithSignature("xcmSend(bytes,bytes)", dest, message)
                    );
                    bytes32 xcmHash = keccak256(message);

                    if (!success) {{
                        emit XcmFailed(xcmHash, returnData);
                        IERC20(tokenAddress).safeTransfer(msg.sender, amount);
                    }} else {{
                        emit XcmSent(msg.sender, keccak256(beneficiaryBytes), amount, xcmHash);
                    }}
                }}

                // ==========================================
                //              ADMIN & UTILS
                // ==========================================

                function setPalletIndex(uint8 _newIndex) external onlyOwner {{
                    palletIndex = _newIndex;
                }}

                function setDefaultWeight(uint64 _newWeight) external onlyOwner {{
                    defaultWeight = _newWeight;
                }}

                function rescueTokens(address token, address to, uint256 amount) external onlyOwner {{
                    if (token == address(0)) payable(to).transfer(amount);
                    else IERC20(token).safeTransfer(to, amount);
                }}

                receive() external payable {{}}
            }}
        """)

class XcmWizard:
    def __init__(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_int_input(self, prompt, default, min_val=None, max_val=None):
        while True:
            val = input(prompt).strip()
            if val == "":
                return default
            try:
                ival = int(val)
                if min_val is not None and ival < min_val:
                    print(f"❌ Minimum value is {min_val}")
                    continue
                if max_val is not None and ival > max_val:
                    print(f"❌ Maximum value is {max_val}")
                    continue
                return ival
            except ValueError:
                print("❌ Must be a number!")

    def get_address_input(self, prompt, default):
        while True:
            val = input(prompt).strip()
            if val == "":
                return default
            if re.match(r'^0x[a-fA-F0-9]{40}$', val):
                return val
            print("❌ Address must start with 0x followed by 40 hex characters")

    def run(self):
        print(Style.HEADER + Style.BOLD + "\n>>> POLKADOT XCM WIZARD v8.0 (PRODUCTION READY) <<<\n" + Style.RESET)
        p_name = input("Project Name      : ") or "DeryBridge"
        author = input("Author            : ") or "Dery"
        
        para_id = self.get_int_input("Target Parachain ID [2004]: ", 2004, 1, 9999)
        pre_addr = self.get_address_input("XCM Precompile Addr [0x0000000000000000000000000000000000000804]: ", "0x0000000000000000000000000000000000000804")
        
        print("\n[1] Ethereum (20 bytes - Moonbeam)\n[2] Substrate (32 bytes - Astar/Polkadot)")
        acc_choice = input("Select account format [1]: ") or "1"
        acc_format = "ethereum" if acc_choice == "1" else "substrate"

        print("\n--- Advanced Options (Press Enter for default) ---")
        pallet_idx = self.get_int_input("Pallet index for ERC-20 [50]: ", 50, 1, 255)
        def_weight = self.get_int_input("Default weight [1000000000]: ", 1000000000, 1, 10**12)

        print("\n[*] Building smart contract...")
        time.sleep(1)

        code = SolidityTemplates.get_xcm_contract(
            p_name, author, para_id, acc_format, pre_addr, pallet_idx, def_weight
        )
        filename = f"{p_name.replace(' ', '')}Bridge.sol"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(code)

        print(f"\n{Style.GREEN}✅ SUCCESS! File: {filename}{Style.RESET}")
        print("📋 Next Steps:")
        print("1. Install OpenZeppelin: `npm install @openzeppelin/contracts`")
        print("2. Deploy with the XCM precompile address parameter")
        print("3. Test on testnet (Moonbase Alpha) before mainnet")
        print("4. Ensure weight is sufficient for your transaction")

if __name__ == "__main__":
    XcmWizard().run()
