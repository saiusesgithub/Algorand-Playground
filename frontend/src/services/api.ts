import axios from 'axios';

// For Vercel deployment - use relative /api paths
const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// API Types
export interface NetworkStatus {
    status: string;
    current_round: number;
    network: string;
    connected: boolean;
}

export interface Account {
    address: string;
    mnemonic?: string;
}

export interface Balance {
    address: string;
    balance_algo: number;
    balance_microalgos: number;
    min_balance_algo: number;
    available_algo: number;
    status: string;
    round: number;
}

export interface Transaction {
    transaction_id: string;
    confirmed_round?: number;
    sender?: string;
    receiver?: string;
    amount_algo?: number;
    fee_algo?: number;
    note?: string;
}

export interface TransactionHistory {
    address: string;
    transactions: any[];
    count: number;
}

// API Service - Updated for Vercel serverless functions
export const algorandAPI = {
    // Network
    getNetworkStatus: async (): Promise<NetworkStatus> => {
        const response = await api.get('/network-status');
        return response.data;
    },

    // Accounts
    createAccount: async (): Promise<Account & { success: boolean; message: string }> => {
        const response = await api.post('/create-account');
        return response.data;
    },

    recoverAccount: async (mnemonic: string): Promise<Account & { success: boolean; message: string }> => {
        const response = await api.post('/recover-account', { mnemonic });
        return response.data;
    },

    getBalance: async (address: string): Promise<Balance> => {
        const response = await api.get(`/balance?address=${encodeURIComponent(address)}`);
        return response.data;
    },

    // Transactions
    sendTransaction: async (
        senderMnemonic: string,
        receiverAddress: string,
        amountAlgo: number,
        note?: string
    ): Promise<{ success: boolean; transaction_id?: string; confirmed_round?: number; message: string }> => {
        const response = await api.post('/send-transaction', {
            sender_mnemonic: senderMnemonic,
            receiver_address: receiverAddress,
            amount_algo: amountAlgo,
            note,
        });
        return response.data;
    },

    getTransactionStatus: async (txid: string): Promise<Transaction & { confirmed: boolean }> => {
        const response = await api.get(`/transaction-status?txid=${encodeURIComponent(txid)}`);
        return response.data;
    },

    getTransactionHistory: async (address: string, limit: number = 10): Promise<TransactionHistory> => {
        const response = await api.get(`/transaction-history?address=${encodeURIComponent(address)}&limit=${limit}`);
        return response.data;
    },
};

export default api;
