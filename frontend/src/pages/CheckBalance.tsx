import { useState } from 'react';
import { algorandAPI, Balance } from '../services/api';
import './Pages.css';

function CheckBalance() {
    const [address, setAddress] = useState('');
    const [balance, setBalance] = useState<Balance | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleCheckBalance = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!address.trim()) return;

        try {
            setLoading(true);
            setError('');
            const result = await algorandAPI.getBalance(address.trim());
            setBalance(result);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to fetch balance');
            setBalance(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page fade-in">
            <div className="page-header">
                <div>
                    <h1 className="page-title">💰 Check Balance</h1>
                    <p className="page-subtitle">View account balance and status</p>
                </div>
            </div>

            <form onSubmit={handleCheckBalance} className="form-card">
                <div className="form-group">
                    <label htmlFor="address">
                        <span>📍</span>
                        Algorand Address
                    </label>
                    <input
                        id="address"
                        type="text"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        placeholder="Enter 58-character Algorand address"
                        required
                    />
                    <span className="input-hint">Example: AAAA...ZZZZ (58 characters)</span>
                </div>

                {error && (
                    <div className="error-message">
                        <span>❌ {error}</span>
                    </div>
                )}

                <button type="submit" disabled={loading} className="primary-btn">
                    {loading ? (
                        <>
                            <span className="spinner"></span>
                            Checking...
                        </>
                    ) : (
                        <>Check Balance</>
                    )}
                </button>
            </form>

            {balance && (
                <div className="result-section">
                    <div className="balance-card">
                        <div className="balance-header">
                            <h2>Account Balance</h2>
                            <span className={`status-badge status-${balance.status.toLowerCase()}`}>
                                {balance.status}
                            </span>
                        </div>

                        <div className="balance-main">
                            <div className="balance-amount">
                                <span className="balance-value">{balance.balance_algo.toFixed(6)}</span>
                                <span className="balance-currency">ALGO</span>
                            </div>
                            <div className="balance-microalgos">
                                {balance.balance_microalgos.toLocaleString()} microAlgos
                            </div>
                        </div>

                        <div className="balance-details">
                            <div className="detail-row">
                                <span className="detail-label">Available Balance:</span>
                                <span className="detail-value text-success">
                                    {balance.available_algo.toFixed(6)} ALGO
                                </span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Minimum Balance:</span>
                                <span className="detail-value text-warning">
                                    {balance.min_balance_algo.toFixed(6)} ALGO
                                </span>
                            </div>
                            <div className="detail-row">
                                <span className="detail-label">Current Round:</span>
                                <span className="detail-value">{balance.round.toLocaleString()}</span>
                            </div>
                        </div>

                        <div className="address-display">
                            <strong>Address:</strong>
                            <code className="address-code">{balance.address}</code>
                        </div>

                        {balance.balance_algo === 0 && (
                            <div className="info-box">
                                <h4>💡 Get Test ALGO</h4>
                                <p>This account has zero balance. Get free test ALGO:</p>
                                <a
                                    href="https://bank.testnet.algorand.network/"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-link"
                                >
                                    Visit TestNet Dispenser →
                                </a>
                            </div>
                        )}

                        <div className="actions-row">
                            <a href={`https://testnet.algoexplorer.io/address/${balance.address}`} target="_blank" rel="noopener noreferrer" className="secondary-btn">
                                🔍 View on Explorer
                            </a>
                            <a href="/send-transaction" className="primary-btn">
                                💸 Send ALGO
                            </a>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CheckBalance;
