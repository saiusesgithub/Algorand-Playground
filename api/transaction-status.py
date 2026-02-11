"""
Vercel Serverless Function: Transaction Status
GET /api/transaction-status?txid=XXXX
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import base64
from urllib.parse import parse_qs, urlparse

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.algod_client import get_algod_client
from utils.helpers import microalgos_to_algos

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            query = urlparse(self.path).query
            params = parse_qs(query)
            txid = params.get('txid', [None])[0]
            
            if not txid:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Transaction ID is required"}).encode())
                return
            
            client = get_algod_client()
            
            # Get pending transaction info
            pending_info = client.pending_transaction_info(txid)
            
            confirmed_round = pending_info.get('confirmed-round', 0)
            
            # Extract transaction details
            txn_data = pending_info.get('txn', {}).get('txn', {})
            
            sender = txn_data.get('snd', None)
            receiver = txn_data.get('rcv', None)
            amount = txn_data.get('amt', 0)
            fee = txn_data.get('fee', 0)
            note = txn_data.get('note', None)
            
            # Try to decode note
            note_text = None
            if note:
                try:
                    note_text = base64.b64decode(note).decode('utf-8')
                except:
                    pass
            
            response = {
                "transaction_id": txid,
                "confirmed": confirmed_round > 0,
                "confirmed_round": confirmed_round if confirmed_round > 0 else None,
                "sender": sender,
                "receiver": receiver,
                "amount_algo": microalgos_to_algos(amount) if amount > 0 else None,
                "fee_algo": microalgos_to_algos(fee) if fee > 0 else None,
                "note": note_text
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "transaction not found" in error_msg:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
