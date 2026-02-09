"""
Recover Algorand Account from Mnemonic

This script recovers an existing Algorand account using its 25-word mnemonic phrase.

Use this when you want to:
- Restore access to an existing account
- Import an account from another wallet
- Verify that a mnemonic is correct
"""

from algosdk import account, mnemonic
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.algod_client import get_algod_client
from utils.helpers import print_account_info, microalgos_to_algos


def recover_account_from_mnemonic(mnemonic_phrase):
    """
    Recovers an account from a 25-word mnemonic phrase.
    
    The mnemonic is a human-readable representation of the private key.
    It can be used to regenerate the exact same private key and address.
    
    Args:
        mnemonic_phrase: String containing 25 words separated by spaces
        
    Returns:
        tuple: (private_key, address) or (None, None) if invalid
    """
    try:
        # Validate and convert mnemonic to private key
        # This will raise an exception if the mnemonic is invalid
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        
        # Derive the public address from the private key
        address = account.address_from_private_key(private_key)
        
        return private_key, address
        
    except Exception as e:
        print(f"\n❌ Error: Invalid mnemonic phrase")
        print(f"   Details: {str(e)}")
        print("\n   Common issues:")
        print("   • Make sure you have exactly 25 words")
        print("   • Check for typos in the words")
        print("   • Ensure words are separated by single spaces")
        print("   • All words should be lowercase")
        return None, None


def verify_account_connection(address):
    """
    Connects to the network and fetches account information.
    
    This verifies that:
    - We can connect to the Algorand network
    - The account exists on the blockchain
    - We can retrieve its current balance
    
    Args:
        address: Account address to check
        
    Returns:
        dict: Account information or None if error
    """
    try:
        client = get_algod_client()
        account_info = client.account_info(address)
        return account_info
    except Exception as e:
        print(f"\n⚠️  Warning: Could not fetch account info from network")
        print(f"   Reason: {str(e)}")
        print("\n   This might mean:")
        print("   • You're offline")
        print("   • The TestNet node is temporarily unavailable")
        print("   • The account hasn't been funded yet (new accounts won't appear)")
        return None


def display_recovery_result(address, mnemonic_phrase, account_info):
    """
    Displays the recovered account information.
    
    Args:
        address: Recovered address
        mnemonic_phrase: Original mnemonic phrase
        account_info: Account information from network (can be None)
    """
    print("\n" + "=" * 70)
    print("ACCOUNT SUCCESSFULLY RECOVERED")
    print("=" * 70)
    
    print("\n📍 RECOVERED ADDRESS:")
    print(f"   {address}")
    
    print("\n🔑 MNEMONIC PHRASE:")
    print("-" * 70)
    words = mnemonic_phrase.split()
    for i in range(0, len(words), 5):
        chunk = words[i:i+5]
        formatted = "   " + "  ".join(f"{i+j+1:2d}. {word:12s}" for j, word in enumerate(chunk))
        print(formatted)
    print("-" * 70)
    
    # Display network account info if available
    if account_info:
        balance = account_info.get('amount', 0)
        status = account_info.get('status', 'Unknown')
        round_num = account_info.get('round', 'N/A')
        
        print("\n💰 ACCOUNT STATUS FROM NETWORK:")
        print(f"   Balance: {microalgos_to_algos(balance):.6f} ALGO")
        print(f"   Status:  {status}")
        print(f"   Round:   {round_num}")
        
        if balance == 0:
            print("\n   ℹ️  This account has zero balance.")
            print("   • Fund it at: https://bank.testnet.algorand.network/")
    else:
        print("\n   ℹ️  Account recovered but network check failed (see warning above)")
    
    print("\n✅ NEXT STEPS:")
    print("   • Check balance: python scripts/check_balance.py <address>")
    print("   • Send transactions using this account")
    print("   • Deploy smart contracts")
    
    print("\n⚠️  SECURITY REMINDER:")
    print("   • Keep your mnemonic secure and private")
    print("   • Never share it or store it digitally")
    
    print("\n" + "=" * 70)


def get_mnemonic_input():
    """
    Prompts user to input their mnemonic phrase.
    
    Provides helpful instructions and validation.
    
    Returns:
        str: The mnemonic phrase
    """
    print("\n📝 ENTER YOUR 25-WORD MNEMONIC PHRASE")
    print("=" * 70)
    print("You can enter it in several ways:")
    print("  1. All on one line, separated by spaces")
    print("  2. Paste from a file")
    print("  3. Type each word (press Enter after typing all 25)")
    print("\nExample format:")
    print("  word1 word2 word3 ... word24 word25")
    print("=" * 70)
    
    mnemonic_phrase = input("\nEnter mnemonic: ").strip()
    
    # Basic validation
    word_count = len(mnemonic_phrase.split())
    if word_count != 25:
        print(f"\n⚠️  Warning: You entered {word_count} words, but a valid mnemonic has 25 words.")
        confirm = input("Continue anyway? (yes/no): ").strip().lower()
        if confirm != 'yes':
            return None
    
    return mnemonic_phrase


def main():
    """Main execution function."""
    print("\n🔓 ALGORAND ACCOUNT RECOVERY")
    print("=" * 70)
    print("This script recovers an Algorand account from its mnemonic phrase.")
    print("=" * 70)
    
    # Get mnemonic from user
    mnemonic_phrase = get_mnemonic_input()
    
    if not mnemonic_phrase:
        print("\n❌ Recovery cancelled.")
        return
    
    # Attempt recovery
    print("\n⏳ Recovering account from mnemonic...")
    private_key, address = recover_account_from_mnemonic(mnemonic_phrase)
    
    if not address:
        print("\n❌ Account recovery failed. Please check your mnemonic and try again.")
        return
    
    # Verify connection to network
    print("\n⏳ Verifying account on TestNet...")
    account_info = verify_account_connection(address)
    
    # Display results
    display_recovery_result(address, mnemonic_phrase, account_info)
    
    print("\n✅ Recovery complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
