"""
Transaction Status Checker

This script allows you to check the status of an Algorand transaction
using its transaction ID.

Use this to:
- Verify if a transaction was confirmed
- Get detailed transaction information
- Check the block/round number
- View transaction parameters
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.algod_client import get_algod_client
from utils.helpers import microalgos_to_algos, format_address


def get_transaction_status(client, txid):
    """
    Retrieves the status and details of a transaction.
    
    This checks both:
    - Pending transactions (not yet confirmed)
    - Confirmed transactions (included in a block)
    
    Args:
        client: AlgodClient instance
        txid: Transaction ID string
        
    Returns:
        tuple: (status_dict, is_confirmed)
    """
    try:
        # First, try to get pending transaction info
        pending_info = client.pending_transaction_info(txid)
        
        # Check if transaction is confirmed
        confirmed_round = pending_info.get('confirmed-round', 0)
        
        if confirmed_round > 0:
            # Transaction is confirmed
            return pending_info, True
        else:
            # Transaction is still pending
            return pending_info, False
            
    except Exception as e:
        error_msg = str(e).lower()
        
        if "not found" in error_msg or "transaction not found" in error_msg:
            print(f"\n❌ Transaction not found: {txid}")
            print("\n   Possible reasons:")
            print("   • Transaction ID is incorrect")
            print("   • Transaction is too old (expired from pending pool)")
            print("   • Transaction was never submitted")
            return None, False
        else:
            print(f"\n❌ Error retrieving transaction: {str(e)}")
            return None, False


def display_pending_transaction(txn_info):
    """
    Displays information about a pending (unconfirmed) transaction.
    
    Args:
        txn_info: Transaction information dictionary
    """
    print("\n" + "=" * 70)
    print("TRANSACTION STATUS: PENDING")
    print("=" * 70)
    
    print("\n⏳ This transaction has been submitted but not yet confirmed.")
    print("   It's waiting to be included in a block.")
    
    # Pool error if any
    pool_error = txn_info.get('pool-error', '')
    if pool_error:
        print(f"\n❌ POOL ERROR: {pool_error}")
        print("   This transaction may have issues and might not confirm.")
    
    print("\n" + "=" * 70)


def display_confirmed_transaction(txn_info, client):
    """
    Displays detailed information about a confirmed transaction.
    
    Args:
        txn_info: Transaction information dictionary
        client: AlgodClient instance for additional queries
    """
    print("\n" + "=" * 70)
    print("TRANSACTION STATUS: CONFIRMED ✓")
    print("=" * 70)
    
    # Basic transaction info
    txid = txn_info.get('txn', {}).get('txn', '')
    confirmed_round = txn_info.get('confirmed-round', 0)
    
    print(f"\n🔖 TRANSACTION ID:")
    print(f"   {txid}")
    
    print(f"\n📦 BLOCK INFORMATION:")
    print(f"   Confirmed in round: {confirmed_round}")
    
    # Get block timestamp if available
    try:
        block = client.block_info(confirmed_round)
        timestamp = block.get('block', {}).get('ts', 0)
        if timestamp:
            from datetime import datetime
            readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f"   Block timestamp:    {readable_time}")
    except:
        pass
    
    # Transaction details
    txn_data = txn_info.get('txn', {}).get('txn', {})
    
    # Payment transaction details
    if 'payment' in txn_data or 'amt' in txn_data:
        sender = txn_data.get('snd', 'Unknown')
        receiver = txn_data.get('rcv', 'Unknown')
        amount = txn_data.get('amt', 0)
        fee = txn_data.get('fee', 0)
        
        print(f"\n💸 PAYMENT DETAILS:")
        print(f"   From:   {sender}")
        print(f"   To:     {receiver}")
        print(f"   Amount: {microalgos_to_algos(amount):.6f} ALGO")
        print(f"   Fee:    {microalgos_to_algos(fee):.6f} ALGO")
    
    # Note if present
    note = txn_data.get('note', None)
    if note:
        try:
            # Try to decode as UTF-8
            note_text = bytes.fromhex(note).decode('utf-8')
            print(f"\n📝 NOTE:")
            print(f"   {note_text}")
        except:
            print(f"\n📝 NOTE (raw):")
            print(f"   {note}")
    
    # Application call details (if applicable)
    if 'appl' in txn_data:
        app_id = txn_data.get('apid', 0)
        print(f"\n📱 APPLICATION CALL:")
        print(f"   Application ID: {app_id}")
    
    # Asset transfer details (if applicable)
    if 'axfer' in txn_data:
        asset_id = txn_data.get('xaid', 0)
        asset_amount = txn_data.get('aamt', 0)
        print(f"\n🪙 ASSET TRANSFER:")
        print(f"   Asset ID: {asset_id}")
        print(f"   Amount:   {asset_amount}")
    
    print(f"\n🔍 VIEW ON EXPLORER:")
    print(f"   https://testnet.algoexplorer.io/tx/{txid}")
    
    print("\n" + "=" * 70)


def main():
    """Main execution function."""
    print("\n🔍 TRANSACTION STATUS CHECKER")
    print("=" * 70)
    
    # Get transaction ID from command line or user input
    if len(sys.argv) > 1:
        txid = sys.argv[1]
        print(f"Checking transaction: {txid[:16]}...")
    else:
        print("Enter the transaction ID to check:")
        print("(Example: 2ZKXVBS2LTHQ5VYHGD34VEKQM3YSHIJJ5ZBMQWWFBFMJ7YDYB7WQ)")
        txid = input("\nTransaction ID: ").strip()
    
    if not txid:
        print("\n❌ No transaction ID provided.")
        return
    
    print("=" * 70)
    
    # Create client
    print("\n⏳ Connecting to Algorand TestNet...")
    client = get_algod_client()
    
    # Get transaction status
    print(f"⏳ Retrieving transaction status...")
    txn_info, is_confirmed = get_transaction_status(client, txid)
    
    if txn_info is None:
        print("\n❌ Could not retrieve transaction information.")
        return
    
    # Display results based on status
    if is_confirmed:
        display_confirmed_transaction(txn_info, client)
        print("\n✅ Transaction successfully confirmed!")
    else:
        display_pending_transaction(txn_info)
        print("\n⏳ Transaction is pending. Check again in a few seconds.")
    
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
