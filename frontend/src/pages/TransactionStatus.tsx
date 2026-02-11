import { useState } from 'react';
import { algorandAPI } from '../services/api';
import './Pages.css';

function TransactionStatus() {
    const [txid, setTxid] = useState('');
    const [status, setStatus] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleCheck = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setLoading(true);
            setError('');
            const result = await algorandAPI.getTransactionStatus(txid.trim());
            setStatus(result);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Transaction not found');
            setStatus(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page fade-in">
            <div className="page-header">
                <h1 className="page-title">📊 Transaction Status</h1>
                <p className="page-subtitle">Check transaction confirmation</p>
            </div>

            <form onSubmit={handleCheck} className="form-card">
                <div className="form-group">
                    <label>Transaction ID</label>
                    <input
                        type="text"
                        value={txid}
                        onChange={(e) => setTxid(e.target.value)}
                        placeholder="Enter transaction ID"
                        required
                    />
                </div>
                {error && <div className="error-message">❌ {error}</div>}
                <button type="submit" disabled={loading} className="primary-btn">
                    {loading ? <><span className="spinner"></span>Checking...</> : <>Check Status</>}
                </button>
            </form>

            {status && (
                <div className="result-section">
                    <div className="balance-card">
                        <h2>{status.confirmed ? '✅ Confirmed' : '⏳ Pending'}</h2>
                        <div className="balance-details">
                            {status.sender && <div className="detail-row"><span>From:</span><code>{status.sender}</code></div>}
                            {status.receiver && <div className="detail-row"><span>To:</span><code>{status.receiver}</code></div>}
                            {status.amount_algo && <div className="detail-row"><span>Amount:</span><span>{status.amount_algo} ALGO</span></div>}
                            {status.confirmed_round && <div className="detail-row"><span>Round:</span><span>{status.confirmed_round}</span></div>}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TransactionStatus;
