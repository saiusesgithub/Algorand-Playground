"""
Helper Utilities for Algorand Development

This module contains reusable utility functions that are used
across multiple scripts in the playground.

These helpers make the code more readable and reduce duplication.
"""

from algosdk import encoding
import json


def microalgos_to_algos(microalgos):
    """
    Converts microAlgos to Algos for human-readable display.
    
    The Algorand blockchain uses microAlgos (1 Algo = 1,000,000 microAlgos)
    as the base unit, similar to how Bitcoin uses satoshis.
    
    Args:
        microalgos: Amount in microAlgos (integer)
        
    Returns:
        float: Amount in Algos
    """
    return microalgos / 1_000_000


def algos_to_microalgos(algos):
    """
    Converts Algos to microAlgos for transaction construction.
    
    When building transactions, amounts must be specified in microAlgos.
    
    Args:
        algos: Amount in Algos (float or int)
        
    Returns:
        int: Amount in microAlgos
    """
    return int(algos * 1_000_000)


def format_address(address):
    """
    Formats an Algorand address for display.
    
    Algorand addresses are 58 characters long. This function displays
    them in a truncated format for readability when needed.
    
    Args:
        address: Full Algorand address
        
    Returns:
        str: Formatted address
    """
    if not address or len(address) < 58:
        return address
    
    return f"{address[:6]}...{address[-6:]}"


def validate_address(address):
    """
    Validates an Algorand address using checksum verification.
    
    Algorand addresses include a checksum to prevent typos.
    This function verifies that an address is valid.
    
    Args:
        address: Address string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # The encoding module will raise an exception if invalid
        encoding.decode_address(address)
        return True
    except Exception:
        return False


def format_transaction_id(txid):
    """
    Formats a transaction ID for display.
    
    Args:
        txid: Transaction ID string
        
    Returns:
        str: Formatted transaction ID
    """
    if not txid or len(txid) < 16:
        return txid
    
    return f"{txid[:8]}...{txid[-8:]}"


def print_account_info(address, balance, client=None):
    """
    Prints formatted account information.
    
    This is a convenience function used by multiple scripts to display
    account details in a consistent format.
    
    Args:
        address: Account address
        balance: Balance in microAlgos
        client: Optional AlgodClient to fetch additional info
    """
    print(f"\nAccount Information:")
    print(f"{'=' * 60}")
    print(f"Address: {address}")
    print(f"Balance: {microalgos_to_algos(balance):.6f} ALGO")
    print(f"         ({balance:,} microAlgos)")
    
    if client:
        try:
            account_info = client.account_info(address)
            print(f"Status: {account_info.get('status', 'Unknown')}")
            print(f"Round: {account_info.get('round', 'N/A')}")
        except Exception as e:
            print(f"Note: Could not fetch additional info ({e})")
    
    print(f"{'=' * 60}")


def print_transaction_summary(txid, sender, receiver, amount, fee, round_num=None):
    """
    Prints a formatted transaction summary.
    
    Args:
        txid: Transaction ID
        sender: Sender address
        receiver: Receiver address
        amount: Amount in microAlgos
        fee: Fee in microAlgos
        round_num: Optional round number
    """
    print(f"\nTransaction Summary:")
    print(f"{'=' * 60}")
    print(f"TX ID: {txid}")
    print(f"From:  {format_address(sender)}")
    print(f"To:    {format_address(receiver)}")
    print(f"Amount: {microalgos_to_algos(amount):.6f} ALGO")
    print(f"Fee:    {microalgos_to_algos(fee):.6f} ALGO")
    
    if round_num:
        print(f"Round:  {round_num}")
    
    print(f"{'=' * 60}")


def wait_for_confirmation(client, txid, timeout=10):
    """
    Waits for a transaction to be confirmed on the blockchain.
    
    After submitting a transaction, you need to wait for it to be
    included in a block. This function polls the network until
    confirmation or timeout.
    
    Args:
        client: AlgodClient instance
        txid: Transaction ID to wait for
        timeout: Number of rounds to wait (default: 10)
        
    Returns:
        dict: Transaction information if confirmed, None if timeout
    """
    print(f"Waiting for confirmation (timeout: {timeout} rounds)...")
    
    try:
        # Get the current round as a starting point
        last_round = client.status().get('last-round')
        current_round = last_round + 1
        timeout_round = current_round + timeout
        
        # Poll until transaction confirms or we timeout
        while current_round < timeout_round:
            try:
                # Check if transaction is confirmed
                pending_txn = client.pending_transaction_info(txid)
                
                if pending_txn.get("confirmed-round", 0) > 0:
                    print(f"✓ Transaction confirmed in round {pending_txn.get('confirmed-round')}")
                    return pending_txn
                
                # Wait for next round
                client.status_after_block(current_round)
                current_round += 1
                
            except Exception as e:
                print(f"Waiting... (round {current_round})")
                current_round += 1
        
        print(f"✗ Transaction not confirmed after {timeout} rounds")
        return None
        
    except Exception as e:
        print(f"Error waiting for confirmation: {e}")
        return None


def get_min_balance_requirement(num_assets=0, num_apps=0):
    """
    Calculates the minimum balance requirement for an account.
    
    Algorand accounts must maintain a minimum balance:
    - Base: 100,000 microAlgos (0.1 ALGO)
    - Each asset: +100,000 microAlgos
    - Each app opt-in: +100,000 microAlgos
    
    This prevents spam and ensures account viability.
    
    Args:
        num_assets: Number of assets held
        num_apps: Number of apps opted into
        
    Returns:
        int: Minimum balance in microAlgos
    """
    base_min_balance = 100_000  # 0.1 ALGO
    asset_min_balance = 100_000  # per asset
    app_min_balance = 100_000    # per app
    
    total = base_min_balance + (num_assets * asset_min_balance) + (num_apps * app_min_balance)
    return total


def pretty_print_json(data):
    """
    Pretty prints JSON data for debugging and display.
    
    Args:
        data: Dictionary or JSON-serializable object
    """
    print(json.dumps(data, indent=2, sort_keys=True))


# Example usage
if __name__ == "__main__":
    print("Helper Utilities Demo")
    print("=" * 60)
    
    # Conversion examples
    print("\n1. Currency Conversion:")
    print(f"   1,000,000 microAlgos = {microalgos_to_algos(1_000_000)} ALGO")
    print(f"   5.5 ALGO = {algos_to_microalgos(5.5):,} microAlgos")
    
    # Address validation
    print("\n2. Address Validation:")
    test_address = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ"
    print(f"   Is '{test_address}' valid? {validate_address(test_address)}")
    
    # Min balance calculation
    print("\n3. Minimum Balance Requirements:")
    print(f"   New account: {microalgos_to_algos(get_min_balance_requirement())} ALGO")
    print(f"   With 3 assets: {microalgos_to_algos(get_min_balance_requirement(3, 0))} ALGO")
    print(f"   With 2 apps: {microalgos_to_algos(get_min_balance_requirement(0, 2))} ALGO")
    
    print("\n" + "=" * 60)
