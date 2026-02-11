"""
Vercel Serverless Function: Send Transaction
POST /api/send-transaction
Body: { "sender_mnemonic": "...", "receiver_address": "...", "amount_algo": 1.5, "note": "..." }
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from algosdk import account, mnemonic, transaction
from utils.algod_client import get_algod_client
from utils.helpers import (
    microalgos_to_algos,
    algos_to_microalgos,
    validate_address,
    wait_for_confirmation
)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            sender_mnemonic = data.get('sender_mnemonic', '').strip()
            receiver_address = data.get('receiver_address', '').strip()
            amount_algo = float(data.get('amount_algo', 0))
            note_text = data.get('note', '').strip()
            
            # Validate inputs
            if not sender_mnemonic or not receiver_address or amount_algo <= 0:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid input parameters"}).encode())
                return
            
            # Recover sender account
            sender_private_key = mnemonic.to_private_key(sender_mnemonic)
            sender_address = account.address_from_private_key(sender_private_key)
            
            # Validate receiver address
            if not validate_address(receiver_address):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid receiver address"}).encode())
                return
            
            # Prevent sending to self
            if sender_address == receiver_address:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Cannot send to the same address"}).encode())
                return
            
            # Convert amount to microAlgos
            amount_microalgos = algos_to_microalgos(amount_algo)
            
            # Get client and params
            client = get_algod_client()
            params = client.suggested_params()
            
            # Verify sender balance
            sender_info = client.account_info(sender_address)
            sender_balance = sender_info.get('amount', 0)
            min_balance = sender_info.get('min-balance', 100_000)
            
            total_needed = amount_microalgos + params.fee + min_balance
            
            if sender_balance < total_needed:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_msg = f"Insufficient balance. Need {microalgos_to_algos(total_needed)} ALGO, have {microalgos_to_algos(sender_balance)} ALGO"
                self.wfile.write(json.dumps({"error": error_msg}).encode())
                return
            
            # Create transaction
            note_bytes = note_text.encode() if note_text else None
            
            txn = transaction.PaymentTxn(
                sender=sender_address,
                sp=params,
                receiver=receiver_address,
                amt=amount_microalgos,
                note=note_bytes
            )
            
            # Sign transaction
            signed_txn = txn.sign(sender_private_key)
            
            # Send transaction
            txid = client.send_transaction(signed_txn)
            
            # Wait for confirmation (with timeout)
            confirmed_txn = wait_for_confirmation(client, txid, timeout=10)
            
            response = {
                "success": True,
                "transaction_id": txid,
                "confirmed_round": confirmed_txn.get('confirmed-round') if confirmed_txn else None,
                "message": "Transaction sent successfully"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
