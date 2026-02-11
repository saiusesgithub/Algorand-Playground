import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const menuItems = [
    { path: '/', label: 'Dashboard', icon: '🏠' },
    { path: '/create-account', label: 'Create Account', icon: '🔐' },
    { path: '/recover-account', label: 'Recover Account', icon: '🔓' },
    { path: '/check-balance', label: 'Check Balance', icon: '💰' },
    { path: '/send-transaction', label: 'Send ALGO', icon: '💸' },
    { path: '/transaction-status', label: 'Transaction Status', icon: '📊' },
    { path: '/transaction-history', label: 'Transaction History', icon: '🔍' },
];

function Sidebar() {
    const location = useLocation();

    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <span className="logo-icon">⚡</span>
                    <h1 className="logo-text">Algorand<br />Playground</h1>
                </div>
                <p className="subtitle">TestNet Explorer</p>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
                    >
                        <span className="nav-icon">{item.icon}</span>
                        <span className="nav-label">{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className="sidebar-footer">
                <a
                    href="https://bank.testnet.algorand.network/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="footer-link"
                >
                    🚰 Get Test ALGO
                </a>
                <a
                    href="https://testnet.algoexplorer.io/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="footer-link"
                >
                    🔎 AlgoExplorer
                </a>
            </div>
        </aside>
    );
}

export default Sidebar;
