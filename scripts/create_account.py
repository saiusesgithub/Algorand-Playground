"""
Create Algorand Account

This script generates a new Algorand account with a private key and mnemonic.

SECURITY WARNING:
- The mnemonic phrase is the ONLY way to recover your account
- Store it securely offline
- NEVER share it or commit it to version control
- Anyone with your mnemonic has FULL control of your account
"""

from algosdk import account, mnemonic
import sys
import os

# Add parent directory to path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import print_account_info, microalgos_to_algos


def create_new_account():
    """
    Generates a new Algorand account.
    
    An account consists of:
    - Private key: 64 bytes of random data (keep secret!)
    - Public address: 58-character string (safe to share)
    - Mnemonic: 25-word backup phrase (keep secret!)
    
    Returns:
        tuple: (private_key, address, mnemonic)
    """
    # Generate a random private key
    # This is cryptographically secure random data
    private_key, address = account.generate_account()
    
    # Convert the private key to a mnemonic phrase
    # This makes it easier for humans to write down and store
    account_mnemonic = mnemonic.from_private_key(private_key)
    
    return private_key, address, account_mnemonic


def display_account_details(address, mnemonic_phrase):
    """
    Displays account information in a user-friendly format.
    
    Args:
        address: The account's public address
        mnemonic_phrase: The 25-word recovery phrase
    """
    print("\n" + "=" * 70)
    print("NEW ALGORAND ACCOUNT CREATED")
    print("=" * 70)
    
    print("\n📍 PUBLIC ADDRESS:")
    print(f"   {address}")
    print("\n   This is your account's public identifier.")
    print("   It's SAFE to share - use it to receive ALGO.")
    
    print("\n🔑 MNEMONIC RECOVERY PHRASE:")
    print("-" * 70)
    
    # Display mnemonic in a formatted grid (easier to write down)
    words = mnemonic_phrase.split()
    for i in range(0, len(words), 5):
        chunk = words[i:i+5]
        formatted = "   " + "  ".join(f"{i+j+1:2d}. {word:12s}" for j, word in enumerate(chunk))
        print(formatted)
    
    print("-" * 70)
    
    print("\n⚠️  CRITICAL SECURITY REMINDERS:")
    print("   1. Write down this 25-word phrase on PAPER")
    print("   2. Store it in a SECURE, OFFLINE location")
    print("   3. NEVER share it with anyone")
    print("   4. NEVER store it in digital files, screenshots, or cloud storage")
    print("   5. Anyone with this phrase has COMPLETE access to your funds")
    print("   6. There is NO password recovery - lose this, lose your account")
    
    print("\n💰 GETTING TEST FUNDS:")
    print("   1. Visit: https://bank.testnet.algorand.network/")
    print("   2. Enter your address above")
    print("   3. Complete the CAPTCHA")
    print("   4. Receive 10 test ALGO (can be done multiple times)")
    
    print("\n✅ NEXT STEPS:")
    print("   • Fund your account using the TestNet dispenser")
    print("   • Check balance: python scripts/check_balance.py <your_address>")
    print("   • Send ALGO: python scripts/send_algo.py")
    
    print("\n" + "=" * 70)


def save_to_file_option(address, mnemonic_phrase):
    """
    Optionally saves account details to a file (FOR TESTNET ONLY).
    
    WARNING: This is only for learning purposes on TestNet.
    NEVER do this with MainNet accounts or real funds!
    
    Args:
        address: Account address
        mnemonic_phrase: Mnemonic phrase
    """
    print("\n❓ Save to file? (TestNet learning only)")
    response = input("   Type 'yes' to save (NOT recommended for security practice): ").strip().lower()
    
    if response == 'yes':
        # Create accounts directory if it doesn't exist
        accounts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "accounts")
        os.makedirs(accounts_dir, exist_ok=True)
        
        # Create filename from first 8 chars of address
        filename = os.path.join(accounts_dir, f"{address[:8]}.account")
        
        with open(filename, 'w') as f:
            f.write(f"Address: {address}\n")
            f.write(f"Mnemonic: {mnemonic_phrase}\n")
            f.write(f"\nWARNING: This file contains sensitive information!\n")
            f.write(f"Only use for TestNet testing. Delete after use.\n")
        
        print(f"\n   ✓ Account saved to: {filename}")
        print(f"   ⚠️  Remember to delete this file when done testing!")
        print(f"   ⚠️  NEVER save MainNet accounts to files!")
    else:
        print("\n   ✓ Account not saved (good security practice!)")


def main():
    """Main execution function."""
    print("\n🚀 ALGORAND ACCOUNT GENERATOR")
    print("=" * 70)
    print("This will create a new Algorand account on TestNet.")
    print("=" * 70)
    
    # Generate the account
    print("\n⏳ Generating random account...")
    private_key, address, mnemonic_phrase = create_new_account()
    
    # Display the details
    display_account_details(address, mnemonic_phrase)
    
    # Optional: save to file (for TestNet learning only)
    save_to_file_option(address, mnemonic_phrase)
    
    print("\n✅ Account creation complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
