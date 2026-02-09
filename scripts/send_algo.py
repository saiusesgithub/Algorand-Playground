"""
Send ALGO Transaction

This script demonstrates how to create, sign, and send a payment transaction
on the Algorand TestNet.

This is one of the most fundamental operations on Algorand:
- Transferring ALGO from one account to another
- Understanding transaction fees
- Waiting for confirmation
"""

from algosdk import transaction, mnemonic, account
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.algod_client import get_algod_client
from utils.helpers import (
    algos_to_microalgos, 
    microalgos_to_algos,
    validate_address,
    wait_for_confirmation,
    print_transaction_summary
)


def get_sender_private_key():
    """
    Prompts user for sender account mnemonic and returns private key.
    
    Returns:
        tuple: (private_key, address) or (None, None) if cancelled
    """
    print("\n🔑 SENDER ACCOUNT")
    print("-" * 70)
    print("Enter the 25-word mnemonic phrase for the account that will SEND ALGO:")
    mnemonic_phrase = input("Mnemonic: ").strip()
    
    # Allow user to cancel
    if not mnemonic_phrase:
        return None, None
    
    try:
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        address = account.address_from_private_key(private_key)
        return private_key, address
    except Exception as e:
        print(f"\n❌ Error: Invalid mnemonic - {str(e)}")
        return None, None


def get_receiver_address():
    """
    Prompts user for receiver address.
    
    Returns:
        str: Receiver address or None if invalid
    """
    print("\n📬 RECEIVER ACCOUNT")
    print("-" * 70)
    print("Enter the address that will RECEIVE the ALGO:")
    receiver = input("Address: ").strip()
    
    if not validate_address(receiver):
        print(f"\n❌ Error: Invalid receiver address format")
        return None
    
    return receiver


def get_amount_to_send():
    """
    Prompts user for amount to send in ALGO.
    
    Returns:
        int: Amount in microAlgos or None if invalid
    """
    print("\n💰 AMOUNT")
    print("-" * 70)
    print("Enter the amount of ALGO to send:")
    print("(e.g., '1.5' for 1.5 ALGO, '0.1' for 0.1 ALGO)")
    
    try:
        amount_input = input("Amount (ALGO): ").strip()
        amount_algos = float(amount_input)
        
        if amount_algos <= 0:
            print(f"\n❌ Error: Amount must be greater than zero")
            return None
        
        amount_microalgos = algos_to_microalgos(amount_algos)
        
        print(f"\n   Converting: {amount_algos} ALGO = {amount_microalgos:,} microAlgos")
        return amount_microalgos
        
    except ValueError:
        print(f"\n❌ Error: Invalid amount format. Please enter a number.")
        return None


def get_optional_note():
    """
    Prompts user for an optional transaction note.
    
    Transaction notes are publicly visible on the blockchain and can be
    used to attach messages or metadata to transactions.
    
    Returns:
        bytes: Encoded note or None
    """
    print("\n📝 NOTE (OPTIONAL)")
    print("-" * 70)
    print("Add an optional note to this transaction:")
    print("(Press Enter to skip)")
    note_input = input("Note: ").strip()
    
    if note_input:
        # Encode the note as bytes
        return note_input.encode()
    return None


def verify_sender_balance(client, sender, amount, fee):
    """
    Verifies that sender has sufficient balance for the transaction.
    
    The sender needs:
    - Amount to send
    - Transaction fee
    - Maintain minimum balance (0.1 ALGO)
    
    Args:
        client: AlgodClient instance
        sender: Sender address
        amount: Amount to send in microAlgos
        fee: Transaction fee in microAlgos
        
    Returns:
        bool: True if sufficient balance, False otherwise
    """
    try:
        account_info = client.account_info(sender)
        balance = account_info.get('amount', 0)
        min_balance = account_info.get('min-balance', 100_000)
        
        total_needed = amount + fee + min_balance
        
        print(f"\n💳 BALANCE CHECK")
        print("-" * 70)
        print(f"Current balance:     {microalgos_to_algos(balance):>10.6f} ALGO")
        print(f"Amount to send:      {microalgos_to_algos(amount):>10.6f} ALGO")
        print(f"Transaction fee:     {microalgos_to_algos(fee):>10.6f} ALGO")
        print(f"Min balance needed:  {microalgos_to_algos(min_balance):>10.6f} ALGO")
        print(f"{'-' * 70}")
        print(f"Total required:      {microalgos_to_algos(total_needed):>10.6f} ALGO")
        
        if balance < total_needed:
            print(f"\n❌ Insufficient balance!")
            print(f"   You need {microalgos_to_algos(total_needed - balance):.6f} more ALGO")
            return False
        
        remaining = balance - total_needed
        print(f"Remaining after:     {microalgos_to_algos(remaining):>10.6f} ALGO")
        print(f"\n✓ Sufficient balance available")
        return True
        
    except Exception as e:
        print(f"\n❌ Error checking balance: {str(e)}")
        return False


def create_payment_transaction(sender, receiver, amount, note, params):
    """
    Creates an unsigned payment transaction.
    
    Args:
        sender: Sender address
        receiver: Receiver address
        amount: Amount in microAlgos
        note: Transaction note (bytes) or None
        params: Suggested transaction parameters
        
    Returns:
        Transaction object
    """
    # Create payment transaction
    # This is the core transaction type on Algorand
    txn = transaction.PaymentTxn(
        sender=sender,
        sp=params,
        receiver=receiver,
        amt=amount,
        note=note
    )
    
    return txn


def sign_transaction(txn, private_key):
    """
    Signs a transaction with the sender's private key.
    
    Signing proves that you own the account and authorize this transaction.
    The signature is cryptographically verified by the network.
    
    Args:
        txn: Transaction object
        private_key: Sender's private key
        
    Returns:
        SignedTransaction object
    """
    signed_txn = txn.sign(private_key)
    return signed_txn


def send_transaction(client, signed_txn):
    """
    Submits a signed transaction to the network.
    
    Args:
        client: AlgodClient instance
        signed_txn: Signed transaction
        
    Returns:
        str: Transaction ID or None if error
    """
    try:
        txid = client.send_transaction(signed_txn)
        return txid
    except Exception as e:
        print(f"\n❌ Error sending transaction: {str(e)}")
        return None


def main():
    """Main execution function."""
    print("\n💸 SEND ALGO TRANSACTION")
    print("=" * 70)
    print("This script will help you send ALGO from one account to another.")
    print("=" * 70)
    
    # Step 1: Get sender credentials
    sender_private_key, sender_address = get_sender_private_key()
    if not sender_address:
        print("\n❌ Transaction cancelled.")
        return
    
    print(f"\n✓ Sender: {sender_address[:8]}...{sender_address[-8:]}")
    
    # Step 2: Get receiver address
    receiver_address = get_receiver_address()
    if not receiver_address:
        print("\n❌ Transaction cancelled.")
        return
    
    print(f"✓ Receiver: {receiver_address[:8]}...{receiver_address[-8:]}")
    
    # Prevent sending to self (common mistake)
    if sender_address == receiver_address:
        print("\n❌ Error: Cannot send to the same address (sender = receiver)")
        return
    
    # Step 3: Get amount
    amount = get_amount_to_send()
    if not amount:
        print("\n❌ Transaction cancelled.")
        return
    
    # Step 4: Get optional note
    note = get_optional_note()
    
    # Step 5: Connect to network and get parameters
    print("\n⏳ Connecting to Algorand TestNet...")
    client = get_algod_client()
    params = client.suggested_params()
    
    # Step 6: Verify balance
    if not verify_sender_balance(client, sender_address, amount, params.fee):
        print("\n❌ Transaction cancelled due to insufficient balance.")
        print("   Get more test ALGO at: https://bank.testnet.algorand.network/")
        return
    
    # Step 7: Confirm transaction
    print("\n⚠️  CONFIRM TRANSACTION")
    print("=" * 70)
    print(f"From:   {sender_address}")
    print(f"To:     {receiver_address}")
    print(f"Amount: {microalgos_to_algos(amount):.6f} ALGO")
    print(f"Fee:    {microalgos_to_algos(params.fee):.6f} ALGO")
    if note:
        print(f"Note:   {note.decode()}")
    print("=" * 70)
    
    confirm = input("\nProceed with transaction? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("\n❌ Transaction cancelled by user.")
        return
    
    # Step 8: Create transaction
    print("\n⏳ Creating transaction...")
    txn = create_payment_transaction(
        sender_address, 
        receiver_address, 
        amount, 
        note, 
        params
    )
    
    # Step 9: Sign transaction
    print("⏳ Signing transaction...")
    signed_txn = sign_transaction(txn, sender_private_key)
    
    # Step 10: Send transaction
    print("⏳ Sending transaction to network...")
    txid = send_transaction(client, signed_txn)
    
    if not txid:
        print("\n❌ Transaction failed to send.")
        return
    
    print(f"\n✓ Transaction sent successfully!")
    print(f"   Transaction ID: {txid}")
    
    # Step 11: Wait for confirmation
    print("\n⏳ Waiting for confirmation on blockchain...")
    confirmed_txn = wait_for_confirmation(client, txid)
    
    if confirmed_txn:
        round_num = confirmed_txn.get('confirmed-round')
        print_transaction_summary(
            txid, 
            sender_address, 
            receiver_address, 
            amount, 
            params.fee,
            round_num
        )
        
        print("\n🔍 View transaction on AlgoExplorer:")
        print(f"   https://testnet.algoexplorer.io/tx/{txid}")
        
        print("\n✅ Transaction complete!")
    else:
        print("\n⚠️  Transaction was sent but confirmation timed out.")
        print("   This doesn't mean it failed - check the explorer:")
        print(f"   https://testnet.algoexplorer.io/tx/{txid}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
