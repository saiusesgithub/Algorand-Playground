"""
Vercel Serverless Function: Transaction History
GET /api/transaction-history?address=XXXX&limit=10
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import parse_qs, urlparse

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.indexer_client import get_indexer_client
from utils.helpers import microalgos_to_algos, validate_address

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            query = urlparse(self.path).query
            params = parse_qs(query)
            address = params.get('address', [None])[0]
            limit = int(params.get('limit', [10])[0])
            
            if not address:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Address parameter is required"}).encode())
                return
            
            # Validate address
            if not validate_address(address):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid Algorand address"}).encode())
                return
            
            # Get indexer client
            indexer = get_indexer_client()
            
            # Search transactions
            response_data = indexer.search_transactions_by_address(address, limit=limit)
            
            transactions = response_data.get('transactions', [])
            
            # Format transactions
            formatted_txns = []
            for txn in transactions:
                formatted_txn = {
                    'id': txn.get('id', ''),
                    'round': txn.get('confirmed-round', 0),
                    'type': txn.get('tx-type', 'unknown'),
                    'timestamp': txn.get('round-time', 0),
                    'sender': txn.get('sender', ''),
                }
                
                # Add payment details if payment transaction
                if txn.get('tx-type') == 'pay':
                    payment_txn = txn.get('payment-transaction', {})
                    formatted_txn['receiver'] = payment_txn.get('receiver', '')
                    formatted_txn['amount_algo'] = microalgos_to_algos(payment_txn.get('amount', 0))
                
                formatted_txns.append(formatted_txn)
            
            result = {
                'address': address,
                'transactions': formatted_txns,
                'count': len(formatted_txns)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
