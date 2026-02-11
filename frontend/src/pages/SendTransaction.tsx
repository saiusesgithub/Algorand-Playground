import { useState } from 'react';
import { algorandAPI } from '../services/api';
import './Pages.css';

function SendTransaction() {
    const [senderMnemonic, setSenderMnemonic] = useState('');
    const [receiverAddress, setReceiverAddress] = useState('');
    const [amount, setAmount] = useState('');
    const [note, setNote] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState<{ transaction_id: string; confirmed_round?: number } | null>(null);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            setLoading(true);
            setError('');
            setResult(null);

            const response = await algorandAPI.sendTransaction(
                senderMnemonic.trim(),
                receiverAddress.trim(),
                parseFloat(amount),
                note.trim() || undefined
            );

            if (response.success && response.transaction_id) {
                setResult({
                    transaction_id: response.transaction_id,
                    confirmed_round: response.confirmed_round,
                });
                // Clear form
                setSenderMnemonic('');
                setReceiverAddress('');
                setAmount('');
                setNote('');
            } else {
                setError(response.message || 'Transaction failed');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to send transaction');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page fade-in">
            <div className="page-header">
                <div>
                    <h1 className="page-title">💸 Send ALGO</h1>
                    <p className="page-subtitle">Transfer ALGO between accounts</p>
                </div>
            </div>

            {!result ? (
                <form onSubmit={handleSend} className="form-card large">
                    <div className="form-group">
                        <label htmlFor="senderMnemonic">
                            <span>🔑</span>
                            Sender Mnemonic (25 words)
                        </label>
                        <textarea
                            id="senderMnemonic"
                            value={senderMnemonic}
                            onChange={(e) => setSenderMnemonic(e.target.value)}
                            placeholder="Enter your 25-word mnemonic phrase"
                            rows={3}
                            required
                        />
                        <span className="input-hint">⚠️ Your mnemonic will never be stored</span>
                    </div>

                    <div className="form-group">
                        <label htmlFor="receiverAddress">
                            <span>📬</span>
                            Receiver Address
                        </label>
                        <input
                            id="receiverAddress"
                            type="text"
                            value={receiverAddress}
                            onChange={(e) => setReceiverAddress(e.target.value)}
                            placeholder="Algorand address to receive ALGO"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="amount">
                            <span>💰</span>
                            Amount (ALGO)
                        </label>
                        <input
                            id="amount"
                            type="number"
                            step="0.000001"
                            min="0.000001"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            placeholder="0.0"
                            required
                        />
                        <span className="input-hint">Minimum: 0.000001 ALGO</span>
                    </div>

                    <div className="form-group">
                        <label htmlFor="note">
                            <span>📝</span>
                            Note (Optional)
                        </label>
                        <input
                            id="note"
                            type="text"
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            placeholder="Optional message (publicly visible)"
                            maxLength={1000}
                        />
                    </div>

                    {error && (
                        <div className="error-message">
                            <span>❌ {error}</span>
                        </div>
                    )}

                    <div className="warning-box">
                        <h4>⚠️ Before Sending</h4>
                        <ul>
                            <li>Verify the receiver address is correct</li>
                            <li>Ensure you have sufficient balance + fees (~0.001 ALGO)</li>
                            <li>Transactions are permanent and cannot be reversed</li>
                            <li>Keep minimum balance of 0.1 ALGO in sender account</li>
                        </ul>
                    </div>

                    <button type="submit" disabled={loading} className="primary-btn large">
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Sending Transaction...
                            </>
                        ) : (
                            <>Send ALGO</>
                        )}
                    </button>
                </form>
            ) : (
                <div className="result-section">
                    <div className="success-card">
                        <div className="success-header">
                            <span className="success-icon">✅</span>
                            <h2>Transaction Sent Successfully!</h2>
                        </div>

                        <div className="result-item">
                            <div className="result-label">
                                <span>🔖</span>
                                <strong>Transaction ID</strong>
                            </div>
                            <div className="result-value">
                                <code>{result.transaction_id}</code>
                            </div>
                        </div>

                        {result.confirmed_round && (
                            <div className="result-item">
                                <div className="result-label">
                                    <span>📦</span>
                                    <strong>Confirmed in Round</strong>
                                </div>
                                <div className="result-value">
                                    <code>{result.confirmed_round.toLocaleString()}</code>
                                </div>
                            </div>
                        )}

                        <div className="success-message">
                            <p>✓ Your transaction has been broadcast to the network</p>
                            {result.confirmed_round ? (
                                <p>✓ Confirmed on the blockchain in round {result.confirmed_round}</p>
                            ) : (
                                <p>⏳ Waiting for blockchain confirmation...</p>
                            )}
                        </div>

                        <div className="actions-row">
                            <a
                                href={`https://testnet.algoexplorer.io/tx/${result.transaction_id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="secondary-btn"
                            >
                                🔍 View on Explorer
                            </a>
                            <a href="/transaction-status" className="secondary-btn">
                                📊 Check Status
                            </a>
                            <button onClick={() => setResult(null)} className="primary-btn">
                                Send Another Transaction
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default SendTransaction;
