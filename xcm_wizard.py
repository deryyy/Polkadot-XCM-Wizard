#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
import textwrap
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
    def print_success(msg):
        print(f"{Style.GREEN}✅ {msg}{Style.RESET}")

    @staticmethod
    def print_info(msg):
        print(f"{Style.BLUE}ℹ️  {msg}{Style.RESET}")

class SolidityTemplates:
    @staticmethod
    def get_xcm_contract(p_name, author, para_id, acc_format, xcm_pre, p_idx, weight):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Account Format Logic
        if acc_format == "ethereum":
            acc_enc = "uint8(1), uint8(0), beneficiaryBytes" # AccountKey20
            len_check = "beneficiaryBytes.length == 20"
            len_err = "Invalid beneficiary length (must be 20 bytes)"
        else:
            acc_enc = "uint8(0), uint8(0), beneficiaryBytes" # AccountId32
            len_check = "beneficiaryBytes.length == 32"
            len_err = "Invalid beneficiary length (must be 32 bytes)"

        return textwrap.dedent(f"""\
            // SPDX-License-Identifier: MIT
            pragma solidity ^0.8.20;

            import "@openzeppelin/contracts/access/Ownable.sol";
            import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
            import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
            import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

            /**
             * @title  {p_name} Universal XCM Bridge
             * @author {author}
             * @notice Generated on {timestamp} via Polkadot XCM Wizard
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
                    require(_xcmPrecompile != address(0), "Invalid precompile address");
                    XCM_PRECOMPILE = _xcmPrecompile;
                }}

                // ==========================================
                //              NATIVE BRIDGE
                // ==========================================
                
                // Overload for ease of use with standard addresses
                function bridgeNative(address beneficiary, uint128 amount) external payable {{
                    bridgeNative(abi.encodePacked(beneficiary), amount);
                }}

                function bridgeNative(bytes memory beneficiaryBytes, uint128 amount) public payable nonReentrant {{
                    require(msg.value >= amount, "Insufficient payment");
                    require({len_check}, "{len_err}");

                    // 1. Construct Destination (MultiLocation)
                    bytes memory dest = abi.encodePacked(
                        uint8(1), uint8(2), uint8(0), uint32(DESTINATION_PARA_ID), {acc_enc}
                    );

                    // 2. Construct Message (Withdraw -> BuyExecution -> Deposit)
                    bytes memory message = abi.encodePacked(
                        uint8(3),                        // WithdrawAsset
                        uint8(1),                        // 1 Asset
                        uint8(0),                        // Here (Native)
                        amount,                          // Amount
                        uint8(4),                        // BuyExecution
                        uint64(defaultWeight),           // Weight Limit
                        uint8(6),                        // DepositAsset
                        uint8(1),                        // 1 Asset
                        uint8(1),                        // Wildcard All
                        beneficiaryBytes                 // Beneficiary
                    );

                    // 3. Send XCM via Precompile
                    (bool success, bytes memory returnData) = XCM_PRECOMPILE.call(
                        abi.encodeWithSignature("xcmSend(bytes,bytes)", dest, message)
                    );
                    
                    bytes32 xcmHash = keccak256(message);

                    if (!success) {{
                        emit XcmFailed(xcmHash, returnData);
                        payable(msg.sender).transfer(amount); // AUTO-REFUND
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
                    require({len_check}, "{len_err}");
                    
                    // Pull tokens from user first
                    IERC20(tokenAddress).safeTransferFrom(msg.sender, address(this), amount);

                    // 1. Construct Destination
                    bytes memory dest = abi.encodePacked(
                        uint8(1), uint8(2), uint8(0), uint32(DESTINATION_PARA_ID), {acc_enc}
                    );

                    // 2. Construct Asset Location (GeneralKey/PalletInstance depending on chain)
                    // Default logic: PalletInstance(50) for Assets pallet
                    bytes memory assetLocation = abi.encodePacked(
                        uint8(1), uint8(2), uint8(3), uint8(palletIndex), uint8(0), uint128(uint160(tokenAddress))
                    );

                    // 3. Construct Message
