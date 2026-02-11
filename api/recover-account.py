"""
Vercel Serverless Function: Recover Account
POST /api/recover-account
Body: { "mnemonic": "25-word phrase" }
"""
from http.server import BaseHTTPRequestHandler
import json
from algosdk import account, mnemonic

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            mnemonic_phrase = data.get('mnemonic', '').strip()
            
            if not mnemonic_phrase:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Mnemonic is required"}).encode())
                return
            
            # Validate and convert mnemonic to private key
            private_key = mnemonic.to_private_key(mnemonic_phrase)
            address = account.address_from_private_key(private_key)
            
            response = {
                "address": address,
                "success": True,
                "message": "Account recovered successfully"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid mnemonic phrase"}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
