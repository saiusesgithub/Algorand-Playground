"""
Counter Smart Contract

This is a stateful smart contract that maintains a global counter.
Users can call the contract to increment the counter value.

This demonstrates:
- Global state storage
- Application calls
- State updates
- OnComplete actions

Key Concepts:
- Global state: Data stored in the application itself
- Local state: Data stored per user who opts in
- Application calls: Transactions that invoke contract logic
"""

from pyteal import *


def counter_contract():
    """
    Creates a stateful counter application.
    
    The contract supports:
    - Creation: Initialize counter to 0
    - Increment: Add 1 to counter (via NoOp call)
    - Delete: Remove the application
    
    Global State:
    - "counter": Integer value starting at 0
    
    Returns:
        Expr: PyTeal approval program
    """
    
    # Define the "counter" key for global state
    counter_key = Bytes("counter")
    
    # Handler for application creation
    # This runs when the application is first deployed
    on_creation = Seq([
        # Initialize the counter at 0
        App.globalPut(counter_key, Int(0)),
        # Approve the creation
        Return(Int(1))
    ])
    
    # Handler for increment operation
    # This runs when someone calls the app with NoOp
    on_increment = Seq([
        # Read current counter value
        # Get current value, add 1, store back
        App.globalPut(
            counter_key,
            App.globalGet(counter_key) + Int(1)
        ),
        # Approve the transaction
        Return(Int(1))
    ])
    
    # Handler for querying the counter (read-only)
    # In practice, you can read global state without calling the contract,
    # but this shows how to structure read operations
    on_query = Return(Int(1))
    
    # Handler for deleting the application
    # Only the creator can delete the app
    on_delete = Return(
        # Check if sender is the creator
        Txn.sender() == Global.creator_address()
    )
    
    # Handler for updating the application
    # Only creator can update
    on_update = Return(
        Txn.sender() == Global.creator_address()
    )
    
    # Main program logic
    # Route to appropriate handler based on OnComplete action
    program = Cond(
        # If this is app creation
        [Txn.application_id() == Int(0), on_creation],
        
        # If this is a NoOp call (normal operation)
        [Txn.on_completion() == OnComplete.NoOp, on_increment],
        
        # If this is delete app
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete],
        
        # If this is update app
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        
        # Reject all other operations (OptIn, CloseOut, ClearState)
        # (Though ClearState should be handled separately)
    )
    
    return program


def clear_state_program():
    """
    Clear state program for the counter contract.
    
    This allows users to remove the app from their account.
    For this simple counter, we don't use local state, so this
    just approves any clear state request.
    
    Returns:
        Expr: PyTeal clear state program
    """
    return Return(Int(1))


def get_global_schema():
    """
    Defines the global state schema for this application.
    
    Global state is stored in the application itself and is
    the same for all users.
    
    Returns:
        tuple: (num_uints, num_byte_slices)
    """
    # We use 1 uint for the counter
    # We use 0 byte slices
    return (1, 0)


def get_local_schema():
    """
    Defines the local state schema for this application.
    
    Local state is stored per user who opts into the application.
    This counter doesn't use local state.
    
    Returns:
        tuple: (num_uints, num_byte_slices)
    """
    # We don't use local state
    return (0, 0)


def compile_contract():
    """
    Compiles the counter contract to TEAL.
    
    Returns:
        tuple: (approval_teal, clear_teal)
    """
    # Compile approval program
    approval_program = counter_contract()
    approval_teal = compileTeal(
        approval_program,
        mode=Mode.Application,
        version=8
    )
    
    # Compile clear state program
    clear_program = clear_state_program()
    clear_teal = compileTeal(
        clear_program,
        mode=Mode.Application,
        version=8
    )
    
    return approval_teal, clear_teal


# For testing/viewing
if __name__ == "__main__":
    print("=" * 70)
    print("COUNTER SMART CONTRACT")
    print("=" * 70)
    
    print("\n📝 CONTRACT DESCRIPTION:")
    print("   A stateful contract that maintains a global counter.")
    print("   Anyone can call it to increment the counter value.")
    
    print("\n📊 STATE SCHEMA:")
    global_schema = get_global_schema()
    local_schema = get_local_schema()
    print(f"   Global: {global_schema[0]} uints, {global_schema[1]} byte slices")
    print(f"   Local:  {local_schema[0]} uints, {local_schema[1]} byte slices")
    
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
    
    print("\n💡 HOW IT WORKS:")
    print("   1. Deploy the contract → counter initialized to 0")
    print("   2. Call with NoOp → counter increments by 1")
    print("   3. Read global state → see current counter value")
    print("   4. Only creator can delete the application")
    
    print("\n🎯 OPERATIONS:")
    print("   • Create:    Initialize counter at 0")
    print("   • NoOp:      Increment counter (+1)")
    print("   • Delete:    Remove app (creator only)")
    print("   • Update:    Upgrade logic (creator only)")
    
    print("\n📚 KEY CONCEPTS:")
    print("   • Global state: Data shared across all users")
    print("   • App.globalPut(): Write to global state")
    print("   • App.globalGet(): Read from global state")
    print("   • Txn.on_completion(): Determines operation type")
    print("   • State schema: Defines storage requirements")
    
    print("\n🚀 NEXT STEPS:")
    print("   • Deploy with deploy/deploy_contract.py")
    print("   • Call the app to increment the counter")
    print("   • Query global state to see counter value")
    
    print("\n" + "=" * 70)
