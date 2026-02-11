import { useState } from 'react';
import { algorandAPI } from '../services/api';
import './Pages.css';

function CreateAccount() {
    const [account, setAccount] = useState<{ address: string; mnemonic: string } | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [copied, setCopied] = useState<'address' | 'mnemonic' | null>(null);

    const handleCreateAccount = async () => {
        try {
            setLoading(true);
            setError('');
            const result = await algorandAPI.createAccount();
            setAccount({ address: result.address, mnemonic: result.mnemonic! });
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to create account');
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = (text: string, type: 'address' | 'mnemonic') => {
        navigator.clipboard.writeText(text);
        setCopied(type);
        setTimeout(() => setCopied(null), 2000);
    };

    return (
        <div className="page fade-in">
            <div className="page-header">
                <div>
                    <h1 className="page-title">🔐 Create Account</h1>
                    <p className="page-subtitle">Generate a new Algorand wallet</p>
                </div>
            </div>

            {!account ? (
                <div className="action-card">
                    <div className="icon-large">🔐</div>
                    <h2>Create New Algorand Account</h2>
                    <p className="text-secondary">
                        Generate a new account with a secure 25-word mnemonic phrase.
                        This phrase is the ONLY way to recover your account - keep it safe!
                    </p>

                    {error && (
                        <div className="error-message">
                            <span>❌ {error}</span>
                        </div>
                    )}

                    <button
                        onClick={handleCreateAccount}
                        disabled={loading}
                        className="primary-btn"
                    >
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Generating...
                            </>
                        ) : (
                            <>Generate Account</>
                        )}
                    </button>

                    <div className="warning-box">
                        <h4>⚠️ Security Warning</h4>
                        <ul>
                            <li>Write down your mnemonic on paper</li>
                            <li>Never share it with anyone</li>
                            <li>Store it in a secure location</li>
                            <li>This is TestNet (practice) only</li>
                        </ul>
                    </div>
                </div>
            ) : (
                <div className="result-section">
                    <div className="success-card">
                        <div className="success-header">
                            <span className="success-icon">✅</span>
                            <h2>Account Created Successfully!</h2>
                        </div>

                        <div className="result-item">
                            <div className="result-label">
                                <span>📍</span>
                                <strong>Public Address</strong>
                            </div>
                            <div className="result-value">
                                <code>{account.address}</code>
                                <button
                                    onClick={() => copyToClipboard(account.address, 'address')}
                                    className="copy-btn"
                                >
                                    {copied === 'address' ? '✓' : '📋'}
                                </button>
                            </div>
                            <p className="result-hint">Safe to share - use this to receive ALGO</p>
                        </div>

                        <div className="result-item mnemonic-section">
                            <div className="result-label">
                                <span>🔑</span>
                                <strong>Mnemonic Recovery Phrase</strong>
                            </div>
                            <div className="mnemonic-grid">
                                {account.mnemonic.split(' ').map((word, index) => (
                                    <div key={index} className="mnemonic-word">
                                        <span className="word-number">{index + 1}</span>
                                        <span className="word-text">{word}</span>
                                    </div>
                                ))}
                            </div>
                            <button
                                onClick={() => copyToClipboard(account.mnemonic, 'mnemonic')}
                                className="copy-mnemonic-btn"
                            >
                                {copied === 'mnemonic' ? '✓ Copied!' : '📋 Copy All Words'}
                            </button>
                            <div className="danger-warning">
                                ⚠️ NEVER share this phrase! Anyone with it has FULL control of your account.
                            </div>
                        </div>

                        <div className="next-steps">
                            <h3>Next Steps:</h3>
                            <ol>
                                <li>
                                    <strong>Fund your account:</strong> Visit{' '}
                                    <a href="https://bank.testnet.algorand.network/" target="_blank" rel="noopener noreferrer">
                                        TestNet Dispenser
                                    </a>
                                </li>
                                <li>
                                    <strong>Check balance:</strong> Go to{' '}
                                    <a href="/check-balance">Check Balance</a>
                                </li>
                                <li>
                                    <strong>Send transactions:</strong> Try{' '}
                                    <a href="/send-transaction">Send ALGO</a>
                                </li>
                            </ol>
                        </div>

                        <button onClick={() => setAccount(null)} className="secondary-btn">
                            Create Another Account
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CreateAccount;
