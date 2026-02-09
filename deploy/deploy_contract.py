"""
Smart Contract Deployment

This script deploys compiled smart contracts to Algorand TestNet.

Deployment process:
1. Compile PyTeal to TEAL (or load compiled TEAL)
2. Compile TEAL to bytecode using Algod
3. Create application creation transaction
4. Sign and submit transaction
5. Wait for confirmation
6. Get application ID

The resulting Application ID is how you reference this
smart contract on the blockchain.
"""

import sys
import os
import base64
import importlib.util

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algosdk import transaction, mnemonic, account
from utils.algod_client import get_algod_client
from utils.helpers import wait_for_confirmation, microalgos_to_algos


def import_contract_module(contract_path):
    """
    Imports a PyTeal contract module.
    
    Args:
        contract_path: Path to contract .py file
        
    Returns:
        module: Imported module or None
    """
    try:
        module_name = os.path.splitext(os.path.basename(contract_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, contract_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"❌ Error importing contract: {str(e)}")
        return None


def compile_to_bytecode(client, source_code):
    """
    Compiles TEAL source code to bytecode using the Algod compiler.
    
    The Algod node provides a compilation service that converts
    TEAL assembly language to the binary bytecode that runs on the AVM.
    
    Args:
        client: AlgodClient instance
        source_code: TEAL source code string
        
    Returns:
        bytes: Compiled bytecode
    """
    try:
        compile_response = client.compile(source_code)
        return base64.b64decode(compile_response['result'])
    except Exception as e:
        print(f"❌ Error compiling TEAL to bytecode: {str(e)}")
        print("   This usually means there's a syntax error in the TEAL code")
        return None


def get_creator_credentials():
    """
    Gets the creator account credentials.
    
    Returns:
        tuple: (private_key, address) or (None, None)
    """
    print("\n🔑 CREATOR ACCOUNT")
    print("-" * 70)
    print("Enter the mnemonic for the account that will CREATE this app:")
    print("(This account will be the app creator and pay the deployment fee)")
    mnemonic_phrase = input("\nMnemonic: ").strip()
    
    if not mnemonic_phrase:
        return None, None
    
    try:
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        address = account.address_from_private_key(private_key)
        return private_key, address
    except Exception as e:
        print(f"❌ Error: Invalid mnemonic - {str(e)}")
        return None, None


def create_app_transaction(
    client,
    creator_address,
    approval_program,
    clear_program,
    global_schema,
    local_schema
):
    """
    Creates an application creation transaction.
    
    Args:
        client: AlgodClient instance
        creator_address: Address of app creator
        approval_program: Compiled approval program (bytes)
        clear_program: Compiled clear state program (bytes)
        global_schema: Tuple of (num_uints, num_byte_slices) for global state
        local_schema: Tuple of (num_uints, num_byte_slices) for local state
        
    Returns:
        Transaction object
    """
    # Get suggested parameters
    params = client.suggested_params()
    
    # Create state schemas
    global_schema = transaction.StateSchema(
        num_uints=global_schema[0],
        num_byte_slices=global_schema[1]
    )
    
    local_schema = transaction.StateSchema(
        num_uints=local_schema[0],
        num_byte_slices=local_schema[1]
    )
    
    # Create the transaction
    txn = transaction.ApplicationCreateTxn(
        sender=creator_address,
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema
    )
    
    return txn


def deploy_contract(contract_path):
    """
    Deploys a smart contract to TestNet.
    
    Args:
        contract_path: Path to the PyTeal contract file
        
    Returns:
        int: Application ID if successful, None otherwise
    """
    print(f"\n⏳ Loading contract: {contract_path}")
    
    # Import and compile the contract
    contract_module = import_contract_module(contract_path)
    if not contract_module:
        return None
    
    if not hasattr(contract_module, 'compile_contract'):
        print("❌ Contract must have 'compile_contract()' function")
        return None
    
    print("⏳ Compiling PyTeal to TEAL...")
    approval_teal, clear_teal = contract_module.compile_contract()
    
    # Get schemas
    global_schema = (0, 0)  # Default
    local_schema = (0, 0)   # Default
    
    if hasattr(contract_module, 'get_global_schema'):
        global_schema = contract_module.get_global_schema()
    if hasattr(contract_module, 'get_local_schema'):
        local_schema = contract_module.get_local_schema()
    
    print(f"   Global Schema: {global_schema[0]} uints, {global_schema[1]} byte slices")
    print(f"   Local Schema:  {local_schema[0]} uints, {local_schema[1]} byte slices")
    
    # Connect to network
    print("\n⏳ Connecting to Algorand TestNet...")
    client = get_algod_client()
    
    # Compile TEAL to bytecode
    print("⏳ Compiling TEAL to bytecode...")
    approval_bytecode = compile_to_bytecode(client, approval_teal)
    clear_bytecode = compile_to_bytecode(client, clear_teal)
    
    if not approval_bytecode or not clear_bytecode:
        return None
    
    print("✅ Bytecode compilation successful")
    
    # Get creator credentials
    creator_private_key, creator_address = get_creator_credentials()
    if not creator_address:
        return None
    
    print(f"✓ Creator: {creator_address[:8]}...{creator_address[-8:]}")
    
    # Check creator balance
    try:
        account_info = client.account_info(creator_address)
        balance = account_info.get('amount', 0)
        print(f"✓ Balance: {microalgos_to_algos(balance):.6f} ALGO")
        
        if balance < 200_000:  # Need at least 0.2 ALGO (0.1 for fee, 0.1 for min)
            print("\n❌ Insufficient balance for deployment")
            print("   You need at least 0.2 ALGO")
            print("   Get test ALGO at: https://bank.testnet.algorand.network/")
            return None
    except Exception as e:
        print(f"❌ Error checking balance: {str(e)}")
        return None
    
    # Create application transaction
    print("\n⏳ Creating application transaction...")
    txn = create_app_transaction(
        client,
        creator_address,
        approval_bytecode,
        clear_bytecode,
        global_schema,
        local_schema
    )
    
    # Sign transaction
    print("⏳ Signing transaction...")
    signed_txn = txn.sign(creator_private_key)
    
    # Confirm deployment
    print("\n⚠️  CONFIRM DEPLOYMENT")
    print("=" * 70)
    print(f"Creator:       {creator_address}")
    print(f"Global Schema: {global_schema}")
    print(f"Local Schema:  {local_schema}")
    print(f"Fee:           ~{microalgos_to_algos(txn.fee):.6f} ALGO")
    print("=" * 70)
    
    confirm = input("\nDeploy contract to TestNet? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("\n❌ Deployment cancelled")
        return None
    
    # Send transaction
    print("\n⏳ Submitting transaction...")
    try:
        txid = client.send_transaction(signed_txn)
        print(f"✓ Transaction sent: {txid}")
    except Exception as e:
        print(f"❌ Error sending transaction: {str(e)}")
        return None
    
    # Wait for confirmation
    print("\n⏳ Waiting for confirmation...")
    confirmed_txn = wait_for_confirmation(client, txid)
    
    if not confirmed_txn:
        print("❌ Deployment failed or timed out")
        return None
    
    # Get application ID
    app_id = confirmed_txn.get('application-index')
    
    return app_id


def main():
    """Main execution function."""
    print("\n🚀 SMART CONTRACT DEPLOYMENT")
    print("=" * 70)
    print("Deploy PyTeal smart contracts to Algorand TestNet")
    print("=" * 70)
    
    # Get contract to deploy
    if len(sys.argv) > 1:
        contract_name = sys.argv[1]
        if not contract_name.endswith('.py'):
            contract_name += '.py'
    else:
        print("\n📁 Available contracts:")
        contracts_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "contracts"
        )
        
        if os.path.exists(contracts_dir):
            contracts = [
                f for f in os.listdir(contracts_dir)
                if f.endswith('.py') and not f.startswith('__')
            ]
            
            for i, contract in enumerate(contracts, 1):
                print(f"   {i}. {contract}")
            
            print("\nEnter contract name or number:")
            choice = input("Contract: ").strip()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(contracts):
                    contract_name = contracts[idx]
                else:
                    print("❌ Invalid choice")
                    return
            else:
                contract_name = choice if choice.endswith('.py') else f"{choice}.py"
        else:
            print("❌ Contracts directory not found")
            return
    
    # Build contract path
    contract_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "contracts",
        contract_name
    )
    
    if not os.path.exists(contract_path):
        print(f"❌ Contract not found: {contract_path}")
        return
    
    # Deploy the contract
    app_id = deploy_contract(contract_path)
    
    if app_id:
        print("\n" + "=" * 70)
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 70)
        print(f"\n🎯 APPLICATION ID: {app_id}")
        print(f"\n   This is your smart contract's unique identifier.")
        print(f"   Use this ID to interact with your contract.")
        
        print(f"\n🔍 View on AlgoExplorer:")
        print(f"   https://testnet.algoexplorer.io/application/{app_id}")
        
        print(f"\n📝 Next Steps:")
        print(f"   • Note down the Application ID: {app_id}")
        print(f"   • Use it to call your contract")
        print(f"   • Query its global state")
        print(f"   • Interact with the application")
        
        print("\n" + "=" * 70)
    else:
        print("\n❌ Deployment failed")
    
    print()


if __name__ == "__main__":
    main()
