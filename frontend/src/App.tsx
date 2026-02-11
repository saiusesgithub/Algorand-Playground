import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import CreateAccount from './pages/CreateAccount';
import RecoverAccount from './pages/RecoverAccount';
import CheckBalance from './pages/CheckBalance';
import SendTransaction from './pages/SendTransaction';
import TransactionStatus from './pages/TransactionStatus';
import TransactionHistory from './pages/TransactionHistory';

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/create-account" element={<CreateAccount />} />
                    <Route path="/recover-account" element={<RecoverAccount />} />
                    <Route path="/check-balance" element={<CheckBalance />} />
                    <Route path="/send-transaction" element={<SendTransaction />} />
                    <Route path="/transaction-status" element={<TransactionStatus />} />
                    <Route path="/transaction-history" element={<TransactionHistory />} />
                </Routes>
            </Layout>
        </Router>
    );
}

export default App;
