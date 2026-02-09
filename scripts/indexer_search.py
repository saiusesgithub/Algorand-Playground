"""
Algorand Indexer Search

This script demonstrates how to use the Algorand Indexer to search
for transactions and account activity.

The Indexer is a separate service that maintains a searchable database
of all blockchain activity. It's much more powerful than querying the
Algod node directly for historical data.

Use this to:
- View transaction history for an address
- Search transactions by type
- Analyze account activity
- Build blockchain analytics
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.indexer_client import get_indexer_client
from utils.helpers import microalgos_to_algos, validate_address, format_address


def search_address_transactions(indexer, address, limit=10, tx_type=None):
    """
    Searches for transactions involving a specific address.
    
    Args:
        indexer: IndexerClient instance
        address: Address to search for
        limit: Maximum number of results (default: 10)
        tx_type: Optional transaction type filter (pay, axfer, acfg, afrz, appl)
        
    Returns:
        dict: Search results containing transactions
    """
    try:
        # Build search parameters
        search_params = {
            'limit': limit
        }
        
        # Add transaction type filter if specified
        if tx_type:
            search_params['txn_type'] = tx_type
        
        # Execute search
        response = indexer.search_transactions_by_address(address, **search_params)
        return response
        
    except Exception as e:
        print(f"\n❌ Error searching transactions: {str(e)}")
        return None


def display_transaction_list(transactions):
    """
    Displays a formatted list of transactions.
    
    Args:
        transactions: List of transaction dictionaries
    """
    if not transactions:
        print("\n   No transactions found for this address.")
        return
    
    print(f"\n   Found {len(transactions)} transaction(s):")
    print("   " + "=" * 66)
    
    for i, txn in enumerate(transactions, 1):
        # Extract transaction details
        txid = txn.get('id', 'Unknown')
        round_num = txn.get('confirmed-round', 0)
        tx_type = txn.get('tx-type', 'unknown')
        
        # Get timestamp if available
        timestamp = txn.get('round-time', 0)
        if timestamp:
            time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            time_str = 'Unknown time'
        
        print(f"\n   [{i}] {time_str}")
        print(f"       Type:  {tx_type.upper()}")
        print(f"       Round: {round_num}")
        print(f"       TX ID: {txid[:16]}...")
        
        # Display details based on transaction type
        if tx_type == 'pay':
            # Payment transaction
            payment_txn = txn.get('payment-transaction', {})
            sender = txn.get('sender', 'Unknown')
            receiver = payment_txn.get('receiver', 'Unknown')
            amount = payment_txn.get('amount', 0)
            
            print(f"       From:  {format_address(sender)}")
            print(f"       To:    {format_address(receiver)}")
            print(f"       Amt:   {microalgos_to_algos(amount):.6f} ALGO")
        
        elif tx_type == 'axfer':
            # Asset transfer
            asset_txn = txn.get('asset-transfer-transaction', {})
            asset_id = asset_txn.get('asset-id', 0)
            amount = asset_txn.get('amount', 0)
            print(f"       Asset: {asset_id}")
            print(f"       Amt:   {amount}")
        
        elif tx_type == 'appl':
            # Application call
            app_txn = txn.get('application-transaction', {})
            app_id = app_txn.get('application-id', 0)
            print(f"       App:   {app_id}")
        
        # Show note if present
        note = txn.get('note', None)
        if note:
            try:
                # Try to decode base64 note
                import base64
                note_text = base64.b64decode(note).decode('utf-8')
                print(f"       Note:  {note_text}")
            except:
                pass
    
    print("\n   " + "=" * 66)


def display_account_summary(indexer, address):
    """
    Displays a summary of account activity from the Indexer.
    
    Args:
        indexer: IndexerClient instance
        address: Address to summarize
    """
    try:
        # Get account information from indexer
        account_info = indexer.account_info(address)
        account = account_info.get('account', {})
        
        balance = account.get('amount', 0)
        created_round = account.get('created-at-round', 0)
        status = account.get('status', 'Unknown')
        
        print(f"\n   📊 ACCOUNT SUMMARY")
        print(f"   {'-' * 66}")
        print(f"   Balance:       {microalgos_to_algos(balance):.6f} ALGO")
        print(f"   Status:        {status}")
        print(f"   Created:       Round {created_round}")
        
        # Asset holdings
        assets = account.get('assets', [])
        if assets:
            print(f"   Assets held:   {len(assets)}")
        
        # Application participation
        apps = account.get('apps-local-state', [])
        if apps:
            print(f"   Apps:          {len(apps)}")
        
        print(f"   {'-' * 66}")
        
    except Exception as e:
        # Account might not exist or indexer might not have data yet
        print(f"\n   ℹ️  Could not fetch account summary: {str(e)}")


def main():
    """Main execution function."""
    print("\n🔎 ALGORAND INDEXER SEARCH")
    print("=" * 70)
    print("Search transaction history using the Algorand Indexer.")
    print("=" * 70)
    
    # Get address from command line or user input
    if len(sys.argv) > 1:
        address = sys.argv[1]
    else:
        print("\nEnter an Algorand address to search:")
        address = input("Address: ").strip()
    
    if not address:
        print("\n❌ No address provided.")
        return
    
    # Validate address
    if not validate_address(address):
        print(f"\n❌ Error: Invalid Algorand address format")
        return
    
    print(f"\nSearching for: {address[:8]}...{address[-8:]}")
    
    # Get search parameters
    print("\nHow many recent transactions to show? (default: 10)")
    limit_input = input("Limit: ").strip()
    limit = int(limit_input) if limit_input.isdigit() else 10
    
    print("\nFilter by transaction type? (leave empty for all)")
    print("Options: pay (payments), axfer (assets), appl (applications)")
    tx_type = input("Type: ").strip().lower() or None
    
    print("\n" + "=" * 70)
    
    # Create indexer client
    print("\n⏳ Connecting to Algorand Indexer...")
    indexer = get_indexer_client()
    
    # Display account summary
    print("⏳ Fetching account summary...")
    display_account_summary(indexer, address)
    
    # Search transactions
    print(f"\n⏳ Searching for {limit} recent transactions...")
    results = search_address_transactions(indexer, address, limit, tx_type)
    
    if not results:
        print("\n❌ Search failed.")
        return
    
    # Display results
    transactions = results.get('transactions', [])
    display_transaction_list(transactions)
    
    # Additional info
    print(f"\n💡 TIPS:")
    print(f"   • View any transaction on: https://testnet.algoexplorer.io/")
    print(f"   • The Indexer maintains full blockchain history")
    print(f"   • Use this for analytics and reporting")
    
    print("\n✅ Search complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
