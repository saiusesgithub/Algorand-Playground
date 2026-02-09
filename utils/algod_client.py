"""
Algorand Client Configuration

This module provides a centralized way to create and configure
an Algod client for interacting with the Algorand blockchain.

The Algod client is used for:
- Submitting transactions
- Checking account balances
- Querying blockchain state
- Compiling smart contracts
"""

from algosdk.v2client import algod
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_algod_client():
    """
    Creates and returns an Algod client configured for TestNet.
    
    The client connects to a public TestNet node provided by AlgoNode.
    This is free to use and doesn't require an API key for basic operations.
    
    Returns:
        algod.AlgodClient: Configured Algod client instance
        
    Environment Variables:
        ALGOD_ADDRESS: The URL of the Algod node (defaults to AlgoNode TestNet)
        ALGOD_TOKEN: Authentication token (empty string for public nodes)
    """
    # Get configuration from environment variables with sensible defaults
    algod_address = os.getenv("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
    algod_token = os.getenv("ALGOD_TOKEN", "")
    
    # Create and return the client
    # Note: Public nodes don't require a token, so we pass an empty string
    client = algod.AlgodClient(algod_token, algod_address)
    
    return client


def get_network_status(client):
    """
    Retrieves and returns current network status information.
    
    This is useful for:
    - Verifying connectivity
    - Getting current block/round number
    - Checking network health
    
    Args:
        client: An AlgodClient instance
        
    Returns:
        dict: Network status information including current round
    """
    try:
        status = client.status()
        return status
    except Exception as e:
        print(f"Error getting network status: {e}")
        return None


def get_suggested_params(client):
    """
    Gets suggested transaction parameters from the network.
    
    These parameters are required for constructing transactions and include:
    - Fee per byte
    - First valid round
    - Last valid round
    - Genesis hash
    - Genesis ID
    
    Args:
        client: An AlgodClient instance
        
    Returns:
        SuggestedParams: Transaction parameters
    """
    try:
        params = client.suggested_params()
        return params
    except Exception as e:
        print(f"Error getting suggested params: {e}")
        return None


# Example usage and testing
if __name__ == "__main__":
    print("Testing Algod Client Connection...")
    print("-" * 50)
    
    # Create client
    client = get_algod_client()
    
    # Get and display network status
    status = get_network_status(client)
    if status:
        print(f"✓ Connected to Algorand TestNet")
        print(f"  Current Round: {status.get('last-round')}")
        print(f"  Catchup Time: {status.get('catchup-time', 0)} ms")
        print(f"  Network: {status.get('catchpoint', 'TestNet')}")
    else:
        print("✗ Failed to connect to network")
    
    # Get suggested params
    params = get_suggested_params(client)
    if params:
        print(f"\n✓ Successfully retrieved transaction parameters")
        print(f"  Fee: {params.fee} microAlgos")
        print(f"  Min Fee: {params.min_fee} microAlgos")
    
    print("-" * 50)
