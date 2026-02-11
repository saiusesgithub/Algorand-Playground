import { useState } from 'react';
import { algorandAPI } from '../services/api';
import './Pages.css';

function RecoverAccount() {
    const [mnemonic, setMnemonic] = useState('');
    const [address, setAddress] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleRecover = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setLoading(true);
            setError('');
            const result = await algorandAPI.recoverAccount(mnemonic.trim());
            setAddress(result.address);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Invalid mnemonic phrase');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page fade-in">
            <div className="page-header">
                <h1 className="page-title">🔓 Recover Account</h1>
                <p className="page-subtitle">Restore account from mnemonic</p>
            </div>

            {!address ? (
                <form onSubmit={handleRecover} className="form-card">
                    <div className="form-group">
                        <label htmlFor="mnemonic">
                            <span>🔑</span>
                            25-Word Mnemonic Phrase
                        </label>
                        <textarea
                            id="mnemonic"
                            value={mnemonic}
                            onChange={(e) => setMnemonic(e.target.value)}
                            placeholder="Enter your 25-word mnemonic phrase"
                            rows={4}
                            required
                        />
                    </div>

                    {error && <div className="error-message">❌ {error}</div>}

                    <button type="submit" disabled={loading} className="primary-btn">
                        {loading ? <><span className="spinner"></span>Recovering...</> : <>Recover Account</>}
                    </button>
                </form>
            ) : (
                <div className="success-card">
                    <div className="success-header">
                        <span className="success-icon">✅</span>
                        <h2>Account Recovered!</h2>
                    </div>
                    <div className="result-item">
                        <div className="result-label"><strong>Address:</strong></div>
                        <div className="result-value"><code>{address}</code></div>
                    </div>
                    <button onClick={() => { setAddress(''); setMnemonic(''); }} className="secondary-btn">
                        Recover Another
                    </button>
                </div>
            )}
        </div>
    );
}

export default RecoverAccount;
