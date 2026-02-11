"""
Vercel Serverless Function: Check Balance
GET /api/balance?address=XXXX
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import parse_qs, urlparse

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.algod_client import get_algod_client
from utils.helpers import microalgos_to_algos, validate_address

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            query = urlparse(self.path).query
            params = parse_qs(query)
            address = params.get('address', [None])[0]
            
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
            
            # Get client and account info
            client = get_algod_client()
            account_info = client.account_info(address)
            
            balance = account_info.get('amount', 0)
            min_balance = account_info.get('min-balance', 100_000)
            
            response = {
                "address": address,
                "balance_algo": microalgos_to_algos(balance),
                "balance_microalgos": balance,
                "min_balance_algo": microalgos_to_algos(min_balance),
                "available_algo": microalgos_to_algos(balance - min_balance),
                "status": account_info.get('status', 'Unknown'),
                "round": account_info.get('round', 0)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_msg = str(e).lower()
            if "no accounts found" in error_msg or "account does not exist" in error_msg:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Account not found. Fund it at https://bank.testnet.algorand.network/"}).encode())
            else:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
