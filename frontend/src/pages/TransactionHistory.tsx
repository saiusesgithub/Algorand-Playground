import { useState } from 'react';
import { algorandAPI } from '../services/api';
import './Pages.css';

function TransactionHistory() {
    const [address, setAddress] = useState('');
    const [history, setHistory] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setLoading(true);
            setError('');
            const result = await algorandAPI.getTransactionHistory(address.trim(), 10);
            setHistory(result);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to fetch history');
            setHistory(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page fade-in">
            <div className="page-header">
                <h1 className="page-title">🔍 Transaction History</h1>
                <p className="page-subtitle">Search blockchain history</p>
            </div>

            <form onSubmit={handleSearch} className="form-card">
                <div className="form-group">
                    <label>Algorand Address</label>
                    <input
                        type="text"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        placeholder="Enter address to search"
                        required
                    />
                </div>
                {error && <div className="error-message">❌ {error}</div>}
                <button type="submit" disabled={loading} className="primary-btn">
                    {loading ? <><span className="spinner"></span>Searching...</> : <>Search History</>}
                </button>
            </form>

            {history && (
                <div className="result-section">
                    <h3>Found {history.count} transaction(s)</h3>
                    {history.transactions.map((tx: any, idx: number) => (
                        <div key={idx} className="transaction-card">
                            <div><strong>Type:</strong> {tx.type.toUpperCase()}</div>
                            <div><strong>Round:</strong> {tx.round}</div>
                            {tx.receiver && <div><strong>To:</strong> <code>{tx.receiver.substring(0, 10)}...</code></div>}
                            {tx.amount_algo && <div><strong>Amount:</strong> {tx.amount_algo} ALGO</div>}
                            <a href={`https://testnet.algoexplorer.io/tx/${tx.id}`} target="_blank" rel="noopener noreferrer" className="inline-link">
                                View Details →
                            </a>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default TransactionHistory;
