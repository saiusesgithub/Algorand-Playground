"""
FastAPI Backend for Algorand Playground
Exposes Python CLI functionality through REST API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our utility functions
from utils.algod_client import get_algod_client, get_network_status
from utils.indexer_client import get_indexer_client
from utils.helpers import (
    microalgos_to_algos,
    algos_to_microalgos,
    validate_address,
    wait_for_confirmation,
    get_min_balance_requirement
)

# Import Algorand SDK
from algosdk import account, mnemonic, transaction

# Create FastAPI app
app = FastAPI(
    title="Algorand Playground API",
    description="REST API for Algorand blockchain operations",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================

class NetworkStatusResponse(BaseModel):
    status: str
    current_round: int
    network: str
    connected: bool

class CreateAccountResponse(BaseModel):
    address: str
    mnemonic: str
    success: bool
    message: str

class RecoverAccountRequest(BaseModel):
    mnemonic: str

class RecoverAccountResponse(BaseModel):
    address: str
    success: bool
    message: str

class BalanceResponse(BaseModel):
    address: str
    balance_algo: float
    balance_microalgos: int
    min_balance_algo: float
    available_algo: float
    status: str
    round: int

class SendTransactionRequest(BaseModel):
    sender_mnemonic: str
    receiver_address: str
    amount_algo: float
    note: Optional[str] = None

class SendTransactionResponse(BaseModel):
    success: bool
    transaction_id: Optional[str]
    confirmed_round: Optional[int]
    message: str

class TransactionStatusResponse(BaseModel):
    transaction_id: str
    confirmed: bool
    confirmed_round: Optional[int]
    sender: Optional[str]
    receiver: Optional[str]
    amount_algo: Optional[float]
    fee_algo: Optional[float]
    note: Optional[str]

class TransactionHistoryResponse(BaseModel):
    address: str
    transactions: List[dict]
    count: int

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """API Root - Health check"""
    return {
        "message": "Algorand Playground API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": [
            "/network/status",
            "/account/create",
            "/account/recover",
            "/account/balance/{address}",
            "/transaction/send",
            "/transaction/status/{txid}",
            "/transaction/history/{address}"
        ]
    }

@app.get("/network/status", response_model=NetworkStatusResponse)
async def network_status():
    """Get Algorand TestNet network status"""
    try:
        client = get_algod_client()
        status = get_network_status(client)
        
        if not status:
            raise HTTPException(status_code=503, detail="Unable to connect to network")
        
        return NetworkStatusResponse(
            status="online",
            current_round=status.get('last-round', 0),
            network="TestNet",
            connected=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/account/create", response_model=CreateAccountResponse)
async def create_account():
    """Generate a new Algorand account"""
    try:
        # Generate new account
        private_key, address = account.generate_account()
        
        # Get mnemonic
        account_mnemonic = mnemonic.from_private_key(private_key)
        
        return CreateAccountResponse(
            address=address,
            mnemonic=account_mnemonic,
            success=True,
            message="Account created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/account/recover", response_model=RecoverAccountResponse)
async def recover_account(request: RecoverAccountRequest):
    """Recover account from mnemonic"""
    try:
        # Validate and convert mnemonic to private key
        private_key = mnemonic.to_private_key(request.mnemonic)
        address = account.address_from_private_key(private_key)
        
        return RecoverAccountResponse(
            address=address,
            success=True,
            message="Account recovered successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid mnemonic phrase")

@app.get("/account/balance/{address}", response_model=BalanceResponse)
async def get_balance(address: str):
    """Get account balance"""
    try:
        # Validate address
        if not validate_address(address):
            raise HTTPException(status_code=400, detail="Invalid Algorand address")
        
        # Get client and account info
        client = get_algod_client()
        account_info = client.account_info(address)
        
        balance = account_info.get('amount', 0)
        min_balance = account_info.get('min-balance', 100_000)
        
        return BalanceResponse(
            address=address,
            balance_algo=microalgos_to_algos(balance),
            balance_microalgos=balance,
            min_balance_algo=microalgos_to_algos(min_balance),
            available_algo=microalgos_to_algos(balance - min_balance),
            status=account_info.get('status', 'Unknown'),
            round=account_info.get('round', 0)
        )
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e).lower()
        if "no accounts found" in error_msg or "account does not exist" in error_msg:
            raise HTTPException(status_code=404, detail="Account not found. Fund it at https://bank.testnet.algorand.network/")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transaction/send", response_model=SendTransactionResponse)
async def send_transaction(request: SendTransactionRequest):
    """Send ALGO transaction"""
    try:
        # Recover sender account
        sender_private_key = mnemonic.to_private_key(request.sender_mnemonic)
        sender_address = account.address_from_private_key(sender_private_key)
        
        # Validate receiver address
        if not validate_address(request.receiver_address):
            raise HTTPException(status_code=400, detail="Invalid receiver address")
        
        # Prevent sending to self
        if sender_address == request.receiver_address:
            raise HTTPException(status_code=400, detail="Cannot send to the same address")
        
        # Convert amount to microAlgos
        amount_microalgos = algos_to_microalgos(request.amount_algo)
        
        if amount_microalgos <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than zero")
        
        # Get client and params
        client = get_algod_client()
        params = client.suggested_params()
        
        # Verify sender balance
        sender_info = client.account_info(sender_address)
        sender_balance = sender_info.get('amount', 0)
        min_balance = sender_info.get('min-balance', 100_000)
        
        total_needed = amount_microalgos + params.fee + min_balance
        
        if sender_balance < total_needed:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient balance. Need {microalgos_to_algos(total_needed)} ALGO, have {microalgos_to_algos(sender_balance)} ALGO"
            )
        
        # Create transaction
        note_bytes = request.note.encode() if request.note else None
        
        txn = transaction.PaymentTxn(
            sender=sender_address,
            sp=params,
            receiver=request.receiver_address,
            amt=amount_microalgos,
            note=note_bytes
        )
        
        # Sign transaction
        signed_txn = txn.sign(sender_private_key)
        
        # Send transaction
        txid = client.send_transaction(signed_txn)
        
        # Wait for confirmation
        confirmed_txn = wait_for_confirmation(client, txid, timeout=10)
        
        if confirmed_txn:
            return SendTransactionResponse(
                success=True,
                transaction_id=txid,
                confirmed_round=confirmed_txn.get('confirmed-round'),
                message="Transaction sent and confirmed successfully"
            )
        else:
            return SendTransactionResponse(
                success=True,
                transaction_id=txid,
                confirmed_round=None,
                message="Transaction sent but confirmation timed out. Check status later."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transaction/status/{txid}", response_model=TransactionStatusResponse)
async def get_transaction_status(txid: str):
    """Get transaction status"""
    try:
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
                import base64
                note_text = base64.b64decode(note).decode('utf-8')
            except:
                pass
        
        return TransactionStatusResponse(
            transaction_id=txid,
            confirmed=confirmed_round > 0,
            confirmed_round=confirmed_round if confirmed_round > 0 else None,
            sender=sender,
            receiver=receiver,
            amount_algo=microalgos_to_algos(amount) if amount > 0 else None,
            fee_algo=microalgos_to_algos(fee) if fee > 0 else None,
            note=note_text
        )
        
    except Exception as e:
        error_msg = str(e).lower()
        if "not found" in error_msg or "transaction not found" in error_msg:
            raise HTTPException(status_code=404, detail="Transaction not found")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transaction/history/{address}")
async def get_transaction_history(address: str, limit: int = 10):
    """Get transaction history for an address"""
    try:
        # Validate address
        if not validate_address(address):
            raise HTTPException(status_code=400, detail="Invalid Algorand address")
        
        # Get indexer client
        indexer = get_indexer_client()
        
        # Search transactions
        response = indexer.search_transactions_by_address(address, limit=limit)
        
        transactions = response.get('transactions', [])
        
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
        
        return {
            'address': address,
            'transactions': formatted_txns,
            'count': len(formatted_txns)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint for deployment platforms
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "algorand-playground-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
