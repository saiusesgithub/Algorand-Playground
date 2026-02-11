import { useEffect, useState } from 'react';
import { algorandAPI, NetworkStatus } from '../services/api';
import './Dashboard.css';

function Dashboard() {
    const [networkStatus, setNetworkStatus] = useState<NetworkStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        loadNetworkStatus();
    }, []);

    const loadNetworkStatus = async () => {
        try {
            setLoading(true);
            const status = await algorandAPI.getNetworkStatus();
            setNetworkStatus(status);
            setError('');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to connect to network');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard fade-in">
            <div className="page-header">
                <div>
                    <h1 className="page-title">Dashboard</h1>
                    <p className="page-subtitle">Welcome to Algorand Playground</p>
                </div>
                <button onClick={loadNetworkStatus} className="refresh-btn">
                    🔄 Refresh
                </button>
            </div>

            {loading ? (
                <div className="loading-container">
                    <div className="spinner"></div>
                    <p>Connecting to Algorand TestNet...</p>
                </div>
            ) : error ? (
                <div className="error-card">
                    <h3>❌ Connection Error</h3>
                    <p>{error}</p>
                    <button onClick={loadNetworkStatus} className="retry-btn">Try Again</button>
                </div>
            ) : networkStatus ? (
                <div className="dashboard-grid">
                    <div className="stat-card">
                        <div className="stat-icon">🌐</div>
                        <div className="stat-content">
                            <h3>Network</h3>
                            <p className="stat-value text-primary">{networkStatus.network}</p>
                            <span className="stat-label">
                                {networkStatus.connected ? '✓ Connected' : '✗ Disconnected'}
                            </span>
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon">🔢</div>
                        <div className="stat-content">
                            <h3>Current Round</h3>
                            <p className="stat-value">{networkStatus.current_round.toLocaleString()}</p>
                            <span className="stat-label">Latest Block</span>
                        </div>
                    </div>

                    <div className="stat-card">
                        <div className="stat-icon">⚡</div>
                        <div className="stat-content">
                            <h3>Status</h3>
                            <p className="stat-value text-success">{networkStatus.status.toUpperCase()}</p>
                            <span className="stat-label">API Status</span>
                        </div>
                    </div>
                </div>
            ) : null}

            <div className="features-section">
                <h2 className="section-title">Quick Actions</h2>
                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon">🔐</div>
                        <h3>Create Account</h3>
                        <p>Generate a new Algorand wallet with secure mnemonic phrase</p>
                        <a href="/create-account" className="feature-link">Get Started →</a>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">💰</div>
                        <h3>Check Balance</h3>
                        <p>View account balance and transaction details</p>
                        <a href="/check-balance" className="feature-link">Check Now →</a>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">💸</div>
                        <h3>Send ALGO</h3>
                        <p>Transfer ALGO tokens between accounts securely</p>
                        <a href="/send-transaction" className="feature-link">Send Transaction →</a>
                    </div>

                    <div className="feature-card">
                        <div className="feature-icon">🔍</div>
                        <h3>Transaction History</h3>
                        <p>Search and view transaction history for any address</p>
                        <a href="/transaction-history" className="feature-link">Explore →</a>
                    </div>
                </div>
            </div>

            <div className="info-section">
                <div className="info-card">
                    <h3>🚰 Need Test ALGO?</h3>
                    <p>Get free test tokens from the Algorand TestNet dispenser</p>
                    <a
                        href="https://bank.testnet.algorand.network/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="external-link"
                    >
                        Visit Dispenser →
                    </a>
                </div>

                <div className="info-card">
                    <h3>🔎 Explore Transactions</h3>
                    <p>View all TestNet transactions on AlgoExplorer</p>
                    <a
                        href="https://testnet.algoexplorer.io/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="external-link"
                    >
                        Open Explorer →
                    </a>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
