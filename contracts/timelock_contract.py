"""
Time Lock Smart Contract

This contract demonstrates time-based logic on Algorand.
It only allows execution after a specific block/round number.

This is useful for:
- Vesting schedules
- Delayed transactions
- Time-based access control
- Escrow with time conditions

Key Concepts:
- Global.latest_timestamp(): Current block timestamp
- Global.round(): Current round number
- Conditional logic based on blockchain state
"""

from pyteal import *


def timelock_contract(unlock_round):
    """
    Creates a time-locked stateless contract.
    
    This contract will reject all transactions until the blockchain
    reaches the specified unlock_round. After that round, it approves.
    
    Args:
        unlock_round: The round number when the contract unlocks
        
    Returns:
        Expr: PyTeal approval program
    """
    
    # The contract logic:
    # Check if current round >= unlock_round
    # If yes, approve (return 1)
    # If no, reject (return 0)
    program = Return(
        Global.round() >= Int(unlock_round)
    )
    
    return program


def timelock_contract_with_receiver(unlock_round, receiver_address):
    """
    Creates a more advanced time-locked contract.
    
    This version not only checks the time, but also ensures
    the transaction is going to a specific receiver.
    
    This is typical for vesting contracts where funds should
    only be released to a specific address after a certain time.
    
    Args:
        unlock_round: The round number when funds can be released
        receiver_address: The only address that can receive funds
        
    Returns:
        Expr: PyTeal approval program
    """
    
    # Convert the receiver address to Algorand address format
    receiver_addr = Addr(receiver_address)
    
    # The contract logic:
    # 1. Check if current round >= unlock_round
    # 2. Check if receiver is the authorized address
    # 3. Both conditions must be true
    program = Return(
        And(
            Global.round() >= Int(unlock_round),
            Txn.receiver() == receiver_addr
        )
    )
    
    return program


def timelock_with_escape_hatch(unlock_round, owner_address):
    """
    Creates a time-locked contract with owner override.
    
    This allows:
    - Normal unlock after specified round
    - Owner can always access (emergency escape)
    
    Args:
        unlock_round: Round when anyone can access
        owner_address: Address that can always access
        
    Returns:
        Expr: PyTeal approval program
    """
    
    owner_addr = Addr(owner_address)
    
    # The contract logic:
    # Approve if EITHER:
    # - Current round >= unlock_round, OR
    # - Sender is the owner
    program = Return(
        Or(
            Global.round() >= Int(unlock_round),
            Txn.sender() == owner_addr
        )
    )
    
    return program


def compile_timelock(unlock_round):
    """
    Compiles a basic timelock contract to TEAL.
    
    Args:
        unlock_round: Round number to unlock at
        
    Returns:
        str: Compiled TEAL code
    """
    program = timelock_contract(unlock_round)
    teal_code = compileTeal(
        program,
        mode=Mode.Signature,  # Stateless contract
        version=8
    )
    
    return teal_code


# For testing/demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("TIME LOCK SMART CONTRACT")
    print("=" * 70)
    
    print("\n📝 CONTRACT DESCRIPTION:")
    print("   A stateless contract that unlocks after a specific round.")
    print("   Before that round, all transactions are rejected.")
    print("   After that round, all transactions are approved.")
    
    # Example: unlock in 1000 rounds from now
    # In practice, you'd calculate this based on desired time
    example_unlock_round = 1000000
    
    print(f"\n⏰ EXAMPLE CONFIGURATION:")
    print(f"   Unlock Round: {example_unlock_round}")
    print(f"   (This is just an example value)")
    
    print("\n🔨 COMPILING BASIC TIMELOCK...")
    teal_code = compile_timelock(example_unlock_round)
    
    print("\n✅ COMPILED TEAL CODE:")
    print("-" * 70)
    print(teal_code)
    print("-" * 70)
    
    print("\n💡 HOW IT WORKS:")
    print("   1. Contract checks: is current_round >= unlock_round?")
    print("   2. If yes → approve transaction (return 1)")
    print("   3. If no → reject transaction (return 0)")
    
    print("\n📊 TEAL EXPLANATION:")
    print("   global LatestTimestamp → Get current block timestamp")
    print("   txn FirstValid → First round this txn is valid")
    print("   int 1000000 → The unlock round number")
    print("   >= → Compare values")
    print("   return → Return result (1=approve, 0=reject)")
    
    print("\n🎯 VARIATIONS:")
    print("   1. Basic Timelock:")
    print("      → Unlocks for everyone after specified round")
    print("\n   2. Timelock with Receiver:")
    print("      → Unlocks only for specific address after round")
    print("\n   3. Timelock with Escape Hatch:")
    print("      → Owner can always access, others wait for unlock")
    
    print("\n⚡ ROUND vs TIMESTAMP:")
    print("   • Rounds: More predictable, ~3.7 seconds per round")
    print("   • Timestamps: Actual Unix time, but less precise")
    print("   • This example uses rounds (Global.round())")
    print("   • Could also use Global.latest_timestamp() for time-based")
    
    print("\n📚 USE CASES:")
    print("   • Vesting schedules (release tokens over time)")
    print("   • Delayed payments (escrow until date)")
    print("   • Time-based access control")
    print("   • Auction end times")
    print("   • Cooldown periods")
    
    print("\n🚀 DEPLOYMENT:")
    print("   • For real use, calculate proper unlock round:")
    print("     current_round = algod.status()['last-round']")
    print("     unlock_round = current_round + desired_delay_rounds")
    print("\n   • Example: 1 hour ≈ 973 rounds (3600s / 3.7s)")
    print("   • Example: 1 day ≈ 23,351 rounds")
    print("   • Example: 1 week ≈ 163,459 rounds")
    
    print("\n" + "=" * 70)
