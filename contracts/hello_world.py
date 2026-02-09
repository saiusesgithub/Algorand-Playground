"""
Hello World Smart Contract

This is the simplest possible smart contract on Algorand.
It's a stateless contract that ALWAYS approves any transaction.

Purpose:
- Learn PyTeal basics
- Understand contract compilation
- See how approval programs work

This contract demonstrates:
- Basic PyTeal syntax
- The approval paradigm
- How to compile contracts to TEAL
"""

from pyteal import *


def hello_world_contract():
    """
    Creates a stateless smart contract that always approves.
    
    In Algorand, smart contracts have two programs:
    1. Approval Program: Logic that must evaluate to True
    2. Clear State Program: Logic for removing app from account
    
    This is the simplest approval program possible.
    
    Returns:
        Expr: PyTeal expression that evaluates to Int(1) (True)
    """
    
    # The contract logic
    # Int(1) means "approve this transaction"
    # Int(0) would mean "reject this transaction"
    program = Return(Int(1))
    
    return program


def clear_state_program():
    """
    Creates a basic clear state program.
    
    The clear state program runs when a user wants to remove
    the application from their account. It should almost always
    approve to allow users to clean up their account state.
    
    Returns:
        Expr: PyTeal expression that approves clear state
    """
    return Return(Int(1))


def compile_contract():
    """
    Compiles the PyTeal contract to TEAL.
    
    This function converts the high-level PyTeal code into
    low-level TEAL assembly language that runs on the AVM
    (Algorand Virtual Machine).
    
    Returns:
        tuple: (approval_teal, clear_teal)
    """
    # Compile approval program
    approval_program = hello_world_contract()
    approval_teal = compileTeal(
        approval_program,
        mode=Mode.Application,
        version=8  # TEAL version 8 (latest stable)
    )
    
    # Compile clear state program
    clear_program = clear_state_program()
    clear_teal = compileTeal(
        clear_program,
        mode=Mode.Application,
        version=8
    )
    
    return approval_teal, clear_teal


# For testing/viewing the contract
if __name__ == "__main__":
    print("=" * 70)
    print("HELLO WORLD SMART CONTRACT")
    print("=" * 70)
    
    print("\n📝 CONTRACT DESCRIPTION:")
    print("   This is a stateless contract that always approves.")
    print("   It's the 'Hello World' of Algorand smart contracts.")
    
    print("\n🔨 COMPILING CONTRACT...")
    approval_teal, clear_teal = compile_contract()
    
    print("\n✅ APPROVAL PROGRAM (TEAL):")
    print("-" * 70)
    print(approval_teal)
    print("-" * 70)
    
    print("\n✅ CLEAR STATE PROGRAM (TEAL):")
    print("-" * 70)
    print(clear_teal)
    print("-" * 70)
    
    print("\n💡 EXPLANATION:")
    print("   The TEAL code you see above is what actually runs on the blockchain.")
    print("   PyTeal is just a Python DSL that generates this TEAL code.")
    print("\n   'int 1' = push integer 1 onto stack")
    print("   'return' = return the top of stack (1 = approve, 0 = reject)")
    
    print("\n📚 KEY CONCEPTS:")
    print("   • Smart contracts on Algorand are written in TEAL")
    print("   • PyTeal lets us write contracts in Python")
    print("   • Approval program: must return 1 to approve transaction")
    print("   • Clear state program: allows users to opt-out of the app")
    
    print("\n🚀 NEXT STEPS:")
    print("   • Use deploy/compile_contract.py to compile this")
    print("   • Use deploy/deploy_contract.py to deploy to TestNet")
    print("   • Learn about stateful contracts with counter_contract.py")
    
    print("\n" + "=" * 70)
