"""
Algorand Indexer Client Configuration

The Indexer is a separate service that provides a searchable history
of all transactions and accounts on the Algorand blockchain.

It's useful for:
- Searching transaction history
- Querying account activity
- Finding specific assets or applications
- Analytics and reporting
"""

from algosdk.v2client import indexer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_indexer_client():
    """
    Creates and returns an Indexer client configured for TestNet.
    
    The Indexer client provides read-only access to historical blockchain data.
    We use AlgoNode's free public Indexer service for TestNet.
    
    Returns:
        indexer.IndexerClient: Configured Indexer client instance
        
    Environment Variables:
        INDEXER_ADDRESS: The URL of the Indexer service
        INDEXER_TOKEN: Authentication token (empty for public indexers)
    """
    # Get configuration from environment with defaults
    indexer_address = os.getenv("INDEXER_ADDRESS", "https://testnet-idx.algonode.cloud")
    indexer_token = os.getenv("INDEXER_TOKEN", "")
    
    # Create and return the indexer client
    client = indexer.IndexerClient(indexer_token, indexer_address)
    
    return client


def get_indexer_health(client):
    """
    Checks the health status of the Indexer service.
    
    This verifies that the Indexer is:
    - Online and responding
    - Up to date with the blockchain
    - Ready to serve queries
    
    Args:
        client: An IndexerClient instance
        
    Returns:
        dict: Health status information
    """
    try:
        health = client.health()
        return health
    except Exception as e:
        print(f"Error checking indexer health: {e}")
        return None


def search_transactions_by_address(client, address, limit=10):
    """
    Searches for transactions involving a specific address.
    
    This is one of the most common Indexer operations, allowing you to
    view the transaction history for any account.
    
    Args:
        client: An IndexerClient instance
        address: Algorand address to search for
        limit: Maximum number of transactions to return
        
    Returns:
        dict: Transaction search results
    """
    try:
        response = client.search_transactions_by_address(address, limit=limit)
        return response
    except Exception as e:
        print(f"Error searching transactions: {e}")
        return None


# Example usage and testing
if __name__ == "__main__":
    print("Testing Indexer Client Connection...")
    print("-" * 50)
    
    # Create indexer client
    client = get_indexer_client()
    
    # Check health
    health = get_indexer_health(client)
    if health:
        print(f"✓ Indexer is healthy")
        print(f"  Status: Online")
        print(f"  Round: {health.get('round', 'N/A')}")
    else:
        print("✗ Failed to connect to indexer")
    
    print("-" * 50)
    print("\nIndexer is ready to search transaction history!")
    print("Use the indexer_search.py script to query transactions.")
