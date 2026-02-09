"""
Check Algorand Account Balance

This script queries the Algorand TestNet to get the current balance
and status of an account.

Use this to:
- Check if funding from the TestNet dispenser was successful
- Monitor your account balance
- Verify account exists on the network
"""

from algosdk import account
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.algod_client import get_algod_client
from utils.helpers import microalgos_to_algos, validate_address


def get_account_balance(client, address):
    """
    Fetches account information from the Algorand network.
    
    This makes an API call to the Algod node to retrieve:
    - Current balance
    - Account status
    - Number of transactions
    - Pending rewards
    - Asset holdings
    - Application state
    
    Args:
        client: AlgodClient instance
        address: Account address to query
        
    Returns:
        dict: Account information or None if error
    """
    try:
        account_info = client.account_info(address)
        return account_info
    except Exception as e:
        print(f"\n❌ Error fetching account information:")
        print(f"   {str(e)}")
        
        # Provide helpful error messages
        if "no accounts found" in str(e).lower():
            print("\n   This account doesn't exist on the network yet.")
            print("   New accounts appear only after receiving their first transaction.")
            print("\n   💡 Fund this account at: https://bank.testnet.algorand.network/")
        
        return None


def display_detailed_balance(address, account_info, client):
    """
    Displays comprehensive account information in a formatted way.
    
    Args:
        address: Account address
        account_info: Account information dictionary
        client: AlgodClient to fetch additional network info
    """
    print("\n" + "=" * 70)
    print("ACCOUNT BALANCE & STATUS")
    print("=" * 70)
    
    # Basic information
    print(f"\n📍 ADDRESS:")
    print(f"   {address}")
    
    # Balance information
    balance = account_info.get('amount', 0)
    min_balance = account_info.get('min-balance', 0)
    
    print(f"\n💰 BALANCE:")
    print(f"   Total:        {microalgos_to_algos(balance):>12.6f} ALGO")
    print(f"                 ({balance:,} microAlgos)")
    print(f"\n   Min Balance:  {microalgos_to_algos(min_balance):>12.6f} ALGO")
    print(f"                 ({min_balance:,} microAlgos)")
    
    # Available balance (total minus minimum required)
    available = balance - min_balance
    print(f"\n   Available:    {microalgos_to_algos(available):>12.6f} ALGO")
    print(f"                 ({available:,} microAlgos)")
    
    # Rewards information
    pending_rewards = account_info.get('pending-rewards', 0)
    if pending_rewards > 0:
        print(f"\n   Pending Rewards: {microalgos_to_algos(pending_rewards):.6f} ALGO")
    
    # Account status
    print(f"\n📊 STATUS:")
    status = account_info.get('status', 'Unknown')
    print(f"   Account Status: {status}")
    print(f"   Round:          {account_info.get('round', 'N/A')}")
    
    # Asset and application information
    num_assets = len(account_info.get('assets', []))
    num_apps = len(account_info.get('apps-local-state', []))
    num_created_apps = len(account_info.get('created-apps', []))
    
    if num_assets > 0 or num_apps > 0 or num_created_apps > 0:
        print(f"\n🔧 HOLDINGS & APPLICATIONS:")
        if num_assets > 0:
            print(f"   Assets held:       {num_assets}")
        if num_apps > 0:
            print(f"   Apps opted into:   {num_apps}")
        if num_created_apps > 0:
            print(f"   Apps created:      {num_created_apps}")
    
    # Network information
    try:
        status = client.status()
        print(f"\n🌐 NETWORK INFO:")
        print(f"   Current Round:  {status.get('last-round', 'N/A')}")
        print(f"   Network:        TestNet")
    except:
        pass
    
    # Helpful tips based on balance
    print(f"\n💡 TIPS:")
    if balance == 0:
        print("   • Your account has no balance yet")
        print("   • Fund it at: https://bank.testnet.algorand.network/")
        print("   • You'll receive 10 test ALGO per dispenser use")
    elif available < 100_000:  # Less than 0.1 ALGO available
        print("   • Your available balance is low")
        print("   • Remember: you need at least 0.1 ALGO minimum balance")
        print("   • Get more test ALGO from the dispenser if needed")
    else:
        print("   • Your account is funded and ready to use!")
        print("   • Try sending ALGO: python scripts/send_algo.py")
    
    print("\n" + "=" * 70)


def main():
    """Main execution function."""
    print("\n💰 ALGORAND BALANCE CHECKER")
    print("=" * 70)
    
    # Get address from command line or user input
    if len(sys.argv) > 1:
        address = sys.argv[1]
        print(f"Checking balance for: {address[:8]}...{address[-8:]}")
    else:
        print("Enter the Algorand address to check:")
        address = input("Address: ").strip()
    
    # Validate address format
    if not validate_address(address):
        print("\n❌ Error: Invalid Algorand address format")
        print("   An Algorand address should be:")
        print("   • 58 characters long")
        print("   • Contain only uppercase letters and numbers")
        print("   • Have a valid checksum")
        print("\n   Example: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ")
        return
    
    print("=" * 70)
    
    # Create client and fetch balance
    print("\n⏳ Connecting to Algorand TestNet...")
    client = get_algod_client()
    
    print("⏳ Fetching account information...")
    account_info = get_account_balance(client, address)
    
    if not account_info:
        print("\n❌ Could not retrieve account information.")
        return
    
    # Display the results
    display_detailed_balance(address, account_info, client)
    
    print("\n✅ Balance check complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
