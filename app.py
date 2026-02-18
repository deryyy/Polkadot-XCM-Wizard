import streamlit as st
import textwrap
from datetime import datetime
import time

# --- CONFIGURATION PAGE (Emoji dihapus total) ---
st.set_page_config(
    page_title="Polkadot XCM Wizard v8.0",
    page_icon="*",
    layout="wide"
)

# --- LOGIC CLASS ---
class SolidityTemplates:
    @staticmethod
    def get_xcm_contract(p_name, author, para_id, acc_format, xcm_pre, p_idx, weight):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        if acc_format == "Ethereum (20 bytes)":
            acc_enc = "uint8(1), uint8(0), beneficiaryBytes"
            len_check = "beneficiaryBytes.length == 20"
            len_err = "Invalid beneficiary length (must be 20 bytes)"
        else:
            acc_enc = "uint8(0), uint8(0), beneficiaryBytes"
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
             * @notice Generated on {timestamp} for Polkadot Solidity Hackathon
             */
            contract {p_name.replace(" ", "")}Bridge is Ownable, ReentrancyGuard {{
                using SafeERC20 for IERC20;

                uint32 public constant DESTINATION_PARA_ID = {para_id};
                address public immutable XCM_PRECOMPILE;
                uint64 public defaultWeight = {weight};
                uint8 public palletIndex = {p_idx};

                event XcmSent(address indexed sender, bytes32 indexed beneficiaryHash, uint256 amount, bytes32 indexed xcmHash);
                event XcmFailed(bytes32 indexed xcmHash, bytes reason);

                constructor(address _xcmPrecompile) Ownable(msg.sender) {{
                    require(_xcmPrecompile != address(0), "Invalid precompile address");
                    XCM_PRECOMPILE = _xcmPrecompile;
                }}

                function bridgeNative(address beneficiary, uint128 amount) external payable {{
                    bridgeNative(abi.encodePacked(beneficiary), amount);
                }}

                function bridgeNative(bytes memory beneficiaryBytes, uint128 amount) public payable nonReentrant {{
                    require(msg.value >= amount, "Insufficient payment");
                    require({len_check}, "{len_err}");

                    bytes memory dest = abi.encodePacked(
                        uint8(1), uint8(2), uint8(0), uint32(DESTINATION_PARA_ID), {acc_enc}
                    );

                    bytes memory message = abi.encodePacked(
                        uint8(3), uint8(1), uint8(0), amount,
                        uint8(4), uint8(1), uint64(defaultWeight),
                        uint8(6), uint8(0), beneficiaryBytes
                    );

                    (bool success, bytes memory returnData) = XCM_PRECOMPILE.call(
                        abi.encodeWithSignature("xcmSend(bytes,bytes)", dest, message)
                    );
                    
                    if (!success) {{
                        emit XcmFailed(keccak256(message), returnData);
                        payable(msg.sender).transfer(amount);
                    }} else {{
                        emit XcmSent(msg.sender, keccak256(beneficiaryBytes), amount, keccak256(message));
                    }}
                }}

                function bridgeERC20(address tokenAddress, address beneficiary, uint128 amount) external nonReentrant {{
                    bridgeERC20(tokenAddress, abi.encodePacked(beneficiary), amount);
                }}

                function bridgeERC20(address tokenAddress, bytes memory beneficiaryBytes, uint128 amount) public nonReentrant {{
                    require({len_check}, "{len_err}");
                    IERC20(tokenAddress).safeTransferFrom(msg.sender, address(this), amount);

                    bytes memory dest = abi.encodePacked(
                        uint8(1), uint8(2), uint8(0), uint32(DESTINATION_PARA_ID), {acc_enc}
                    );

                    bytes memory assetLocation = abi.encodePacked(
                        uint8(1), uint8(2), uint8(3), uint8(palletIndex), uint8(0), uint128(uint160(tokenAddress))
                    );

                    bytes memory message = abi.encodePacked(
                        uint8(3), uint8(1), assetLocation, amount,
                        uint8(4), uint8(1), uint64(defaultWeight),
                        uint8(6), uint8(0), beneficiaryBytes
                    );

                    (bool success, bytes memory returnData) = XCM_PRECOMPILE.call(
                        abi.encodeWithSignature("xcmSend(bytes,bytes)", dest, message)
                    );

                    if (!success) {{
                        emit XcmFailed(keccak256(message), returnData);
                        IERC20(tokenAddress).safeTransfer(msg.sender, amount);
                    }} else {{
                        emit XcmSent(msg.sender, keccak256(beneficiaryBytes), amount, keccak256(message));
                    }}
                }}

                receive() external payable {{}}
            }}
        """)

# --- UI LAYOUT (Hanya Teks Standar) ---
st.title("POLKADOT XCM WIZARD v8.0")
st.write("Professional Tool for Cross-Chain Smart Contracts.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("[ Configuration ]")
    p_name = st.text_input("Project Name", value="DeryBridge")
    author = st.text_input("Author Name", value="Dery")
    para_id = st.number_input("Target Parachain ID", value=2004)
    acc_format = st.selectbox("Account Format", ["Ethereum (20 bytes)", "Substrate (32 bytes)"])
    pre_addr = st.text_input("XCM Precompile Address", value="0x0000000000000000000000000000000000000804")
    
    st.markdown("---")
    pallet_idx = st.number_input("ERC-20 Pallet Index", value=50)
    def_weight = st.number_input("Default Weight", value=1000000000)

    generate_btn = st.button("GENERATE CONTRACT", type="primary", use_container_width=True)

with col2:
    if generate_btn:
        code = SolidityTemplates.get_xcm_contract(p_name, author, para_id, acc_format, pre_addr, pallet_idx, def_weight)
        st.success("SUCCESS: Smart Contract Generated!")
        st.code(code, language="solidity")
        st.download_button("DOWNLOAD .SOL FILE", data=code, file_name=f"{p_name}Bridge.sol")
    else:
        st.info("Fill the form and click GENERATE to see the code.")