"""
Smart Contract Compiler

This script compiles PyTeal smart contracts to TEAL.

TEAL (Transaction Execution Approval Language) is the low-level
language that runs on the Algorand Virtual Machine (AVM).

PyTeal is a Python DSL (Domain Specific Language) that makes it
easier to write TEAL by using Python syntax.

This script:
- Imports a PyTeal contract
- Compiles it to TEAL
- Optionally saves to file
- Shows the compiled output
"""

import sys
import os
import importlib.util

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def import_contract_module(contract_path):
    """
    Dynamically imports a Python contract module.
    
    Args:
        contract_path: Path to the .py contract file
        
    Returns:
        module: The imported Python module
    """
    try:
        # Get module name from file path
        module_name = os.path.splitext(os.path.basename(contract_path))[0]
        
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, contract_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module
        
    except Exception as e:
        print(f"❌ Error importing contract: {str(e)}")
        return None


def compile_contract_file(contract_path):
    """
    Compiles a PyTeal contract file to TEAL.
    
    Args:
        contract_path: Path to the PyTeal contract (.py file)
        
    Returns:
        tuple: (approval_teal, clear_teal, metadata) or (None, None, None)
    """
    print(f"\n⏳ Loading contract from: {contract_path}")
    
    # Import the contract module
    contract_module = import_contract_module(contract_path)
    if not contract_module:
        return None, None, None
    
    # Check if module has compile_contract function
    if not hasattr(contract_module, 'compile_contract'):
        print(f"❌ Error: Contract must have a 'compile_contract()' function")
        return None, None, None
    
    print("⏳ Compiling PyTeal to TEAL...")
    
    # Call the compile function
    try:
        approval_teal, clear_teal = contract_module.compile_contract()
        
        # Get metadata if available
        metadata = {}
        if hasattr(contract_module, 'get_global_schema'):
            metadata['global_schema'] = contract_module.get_global_schema()
        if hasattr(contract_module, 'get_local_schema'):
            metadata['local_schema'] = contract_module.get_local_schema()
        
        return approval_teal, clear_teal, metadata
        
    except Exception as e:
        print(f"❌ Error during compilation: {str(e)}")
        return None, None, None


def save_teal_to_file(contract_name, approval_teal, clear_teal):
    """
    Saves compiled TEAL code to files.
    
    Args:
        contract_name: Name of the contract
        approval_teal: Approval program TEAL code
        clear_teal: Clear state program TEAL code
        
    Returns:
        tuple: (approval_path, clear_path)
    """
    # Create output directory
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "compiled"
    )
    os.makedirs(output_dir, exist_ok=True)
    
    # Create file paths
    approval_path = os.path.join(output_dir, f"{contract_name}_approval.teal")
    clear_path = os.path.join(output_dir, f"{contract_name}_clear.teal")
    
    # Write approval program
    with open(approval_path, 'w') as f:
        f.write(approval_teal)
    
    # Write clear state program
    with open(clear_path, 'w') as f:
        f.write(clear_teal)
    
    return approval_path, clear_path


def display_compilation_result(contract_name, approval_teal, clear_teal, metadata):
    """
    Displays the compilation result in a user-friendly format.
    
    Args:
        contract_name: Name of the contract
        approval_teal: Compiled approval program
        clear_teal: Compiled clear state program
        metadata: Contract metadata (schemas, etc.)
    """
    print("\n" + "=" * 70)
    print(f"COMPILED: {contract_name.upper()}")
    print("=" * 70)
    
    # Display metadata if available
    if metadata:
        if 'global_schema' in metadata:
            g = metadata['global_schema']
            print(f"\n📊 Global Schema: {g[0]} uints, {g[1]} byte slices")
        if 'local_schema' in metadata:
            l = metadata['local_schema']
            print(f"📊 Local Schema:  {l[0]} uints, {l[1]} byte slices")
    
    # Display approval program
    print("\n✅ APPROVAL PROGRAM:")
    print("-" * 70)
    print(approval_teal)
    print("-" * 70)
    print(f"   Size: {len(approval_teal)} bytes")
    print(f"   Lines: {len(approval_teal.splitlines())} lines")
    
    # Display clear state program
    print("\n✅ CLEAR STATE PROGRAM:")
    print("-" * 70)
    print(clear_teal)
    print("-" * 70)
    print(f"   Size: {len(clear_teal)} bytes")
    print(f"   Lines: {len(clear_teal.splitlines())} lines")
    
    print("\n" + "=" * 70)


def list_available_contracts():
    """
    Lists all available contracts in the contracts/ directory.
    """
    contracts_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "contracts"
    )
    
    if not os.path.exists(contracts_dir):
        print(f"❌ Contracts directory not found: {contracts_dir}")
        return []
    
    # Find all .py files
    contracts = [
        f for f in os.listdir(contracts_dir)
        if f.endswith('.py') and not f.startswith('__')
    ]
    
    return contracts


def main():
    """Main execution function."""
    print("\n🔨 SMART CONTRACT COMPILER")
    print("=" * 70)
    print("Compiles PyTeal smart contracts to TEAL")
    print("=" * 70)
    
    # Get contract to compile
    if len(sys.argv) > 1:
        contract_name = sys.argv[1]
        if not contract_name.endswith('.py'):
            contract_name += '.py'
    else:
        # List available contracts
        print("\n📁 Available contracts:")
        contracts = list_available_contracts()
        
        if not contracts:
            print("   No contracts found in contracts/ directory")
            return
        
        for i, contract in enumerate(contracts, 1):
            print(f"   {i}. {contract}")
        
        # Get user choice
        print("\nEnter contract name or number:")
        choice = input("Contract: ").strip()
        
        # Handle numeric choice
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(contracts):
                contract_name = contracts[idx]
            else:
                print("❌ Invalid choice")
                return
        else:
            contract_name = choice if choice.endswith('.py') else f"{choice}.py"
    
    # Build full path to contract
    contract_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "contracts",
        contract_name
    )
    
    # Verify file exists
    if not os.path.exists(contract_path):
        print(f"❌ Contract not found: {contract_path}")
        return
    
    # Compile the contract
    approval_teal, clear_teal, metadata = compile_contract_file(contract_path)
    
    if not approval_teal:
        print("\n❌ Compilation failed")
        return
    
    print("✅ Compilation successful!")
    
    # Display results
    base_name = os.path.splitext(contract_name)[0]
    display_compilation_result(base_name, approval_teal, clear_teal, metadata)
    
    # Ask to save
    print("\n💾 Save compiled TEAL to files?")
    save = input("Save? (yes/no): ").strip().lower()
    
    if save == 'yes':
        approval_path, clear_path = save_teal_to_file(
            base_name,
            approval_teal,
            clear_teal
        )
        print(f"\n✅ Saved compiled files:")
        print(f"   Approval: {approval_path}")
        print(f"   Clear:    {clear_path}")
        
        print("\n🚀 Next Step:")
        print(f"   Deploy with: python deploy/deploy_contract.py")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
