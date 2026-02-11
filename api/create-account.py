"""
Vercel Serverless Function: Create Account
POST /api/create-account
"""
from http.server import BaseHTTPRequestHandler
import json
from algosdk import account, mnemonic

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Generate new account
            private_key, address = account.generate_account()
            account_mnemonic = mnemonic.from_private_key(private_key)
            
            response = {
                "address": address,
                "mnemonic": account_mnemonic,
                "success": True,
                "message": "Account created successfully"
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
