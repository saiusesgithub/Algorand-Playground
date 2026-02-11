"""
Vercel Serverless Function: Network Status
GET /api/network-status
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utils.algod_client import get_algod_client, get_network_status

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            client = get_algod_client()
            status = get_network_status(client)
            
            if not status:
                self.send_error(503, "Unable to connect to network")
                return
            
            response = {
                "status": "online",
                "current_round": status.get('last-round', 0),
                "network": "TestNet",
                "connected": True
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
