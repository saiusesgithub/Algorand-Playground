# Getting Started with Algorand Playground

Welcome! This guide will walk you through your first 10 minutes with the Algorand Playground.

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
# Make sure you're in the project directory
cd algorand-playground

# Install required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed py-algorand-sdk-2.x.x pyteal-0.24.x python-dotenv-1.0.x
```

### 2. Test the Connection

Let's verify you can connect to Algorand TestNet:

```bash
python utils/algod_client.py
```

**Expected output:**
```
Testing Algod Client Connection...
--------------------------------------------------
✓ Connected to Algorand TestNet
  Current Round: 12345678
  ...
```

✅ If you see this, you're connected to the Algorand blockchain!

## 🚀 Your First 5 Minutes with Algorand

### Step 1: Create an Account (1 minute)

```bash
python scripts/create_account.py
```

**What you'll see:**
- A public address (like a bank account number)
- A 25-word mnemonic phrase (like your password)

**⚠️ CRITICAL:** Write down the mnemonic on paper. You'll need it!

**Example output:**
```
📍 PUBLIC ADDRESS:
   XYZ123ABC456...789DEF

🔑 MNEMONIC RECOVERY PHRASE:
   1. word1     2. word2     3. word3   ...  25. word25
```

### Step 2: Fund Your Account (2 minutes)

1. Copy your public address
2. Visit: https://bank.testnet.algorand.network/
3. Paste your address
4. Complete CAPTCHA
5. Click "Dispense"

You'll receive **10 test ALGO** (worth $0 - this is fake money for testing!)

### Step 3: Check Your Balance (1 minute)

```bash
python scripts/check_balance.py YOUR_ADDRESS_HERE
```

Or just run it and paste your address when prompted:

```bash
python scripts/check_balance.py
```

**Expected output:**
```
💰 BALANCE:
   Total:        10.000000 ALGO
   Available:    9.900000 ALGO
```

✅ You now have a funded Algorand TestNet account!

### Step 4: Send Your First Transaction (1 minute)

Create a second account to send to, or use a friend's address:

```bash
python scripts/send_algo.py
```

Follow the prompts:
1. Enter your sender mnemonic (from Step 1)
2. Enter receiver address
3. Enter amount (try 0.5 ALGO)
4. Confirm

**Expected output:**
```
✓ Transaction sent successfully!
✓ Transaction confirmed in round 12345679
```

🎉 **Congratulations!** You just sent your first blockchain transaction!

## 🎯 What You Just Learned

In 5 minutes, you:
- ✅ Created a blockchain account
- ✅ Connected to a live blockchain network
- ✅ Received cryptocurrency
- ✅ Sent a blockchain transaction

This is the foundation of all blockchain development!

## 🔍 Next Steps (Choose Your Path)

### Path 1: Explore More Scripts (Beginner)
```bash
# Check transaction status
python scripts/transaction_status.py YOUR_TX_ID

# Search transaction history
python scripts/indexer_search.py YOUR_ADDRESS

# Recover an account from mnemonic
python scripts/recover_account.py
```

### Path 2: Learn Smart Contracts (Intermediate)
```bash
# View a smart contract
python contracts/hello_world.py

# See a more complex contract
python contracts/counter_contract.py

# Compile a contract
python deploy/compile_contract.py
```

### Path 3: Deploy a Smart Contract (Advanced)
```bash
# Deploy your first smart contract
python deploy/deploy_contract.py

# Choose: hello_world.py
# Enter your mnemonic
# Get an Application ID
```

## 💡 Pro Tips

### Tip 1: Use Tab Completion
Most terminals support tab completion. Type `python scripts/c` then hit TAB.

### Tip 2: Save Your Address
Create a text file with your addresses:
```bash
echo "MY_ADDRESS=YOUR_ADDRESS_HERE" > my_accounts.txt
```

### Tip 3: Get More Test ALGO
You can use the dispenser multiple times:
- https://bank.testnet.algorand.network/

### Tip 4: Explore AlgoExplorer
View your account and transactions visually:
- https://testnet.algoexplorer.io/address/YOUR_ADDRESS

## ❓ Troubleshooting

### "Module not found" error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Connection refused" error
- Check your internet connection
- Public nodes might be temporarily unavailable
- Try again in a few minutes

### "Insufficient balance" error
- Get more test ALGO from dispenser
- Remember: you need 0.1 ALGO minimum balance

### "Invalid mnemonic" error
- Check for typos
- Ensure exactly 25 words
- Words should be lowercase
- Separated by single spaces

## 📚 Learn More

Each script has built-in help. Just run it without arguments:

```bash
python scripts/check_balance.py
# Shows prompts and instructions

python utils/helpers.py
# Shows utility function examples
```

## 🎓 Understanding Key Concepts

### What is a Mnemonic?
- 25 random words that represent your private key
- Can restore your account on any device
- **Keep it secret!** Anyone with it controls your account

### What is TestNet?
- A fake blockchain for testing
- ALGO has no real value
- Safe to experiment
- Resets periodically

### What is a Transaction?
- Transfer of ALGO between accounts
- Costs ~0.001 ALGO in fees
- Confirmed in ~3.7 seconds
- Permanent and immutable

### What is a Smart Contract?
- Code that runs on the blockchain
- Enforces rules automatically
- Deployed once, runs forever
- Costs ALGO to deploy

## ✅ Checklist

After following this guide, you should be able to:

- [x] Install the playground
- [x] Create an Algorand account
- [x] Get test ALGO from dispenser
- [x] Check account balance
- [x] Send ALGO transactions
- [x] Understand mnemonics and security
- [x] Navigate the project structure

## 🚀 Ready for More?

Read the full [README.md](README.md) for:
- Complete feature documentation
- Security best practices
- Smart contract deep-dives
- Advanced usage patterns
- Learning resources

---

**Welcome to Algorand development! 🎉**

You're now part of a growing ecosystem of blockchain builders.

Need help? Check out:
- Discord: https://discord.gg/algorand
- Forum: https://forum.algorand.org/
- Docs: https://developer.algorand.org/
