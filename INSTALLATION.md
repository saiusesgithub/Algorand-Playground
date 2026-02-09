# Installation & Setup Guide

This guide will help you set up the Algorand Playground on your system.

## Prerequisites Checklist

Before you begin, ensure you have:

- [x] **Python 3.10 or higher** installed
- [x] **pip** (Python package manager)
- [x] **Internet connection** (for blockchain connectivity)
- [x] **Terminal/Command Prompt** access

## Step-by-Step Installation

### Step 1: Verify Python Installation

Open your terminal and run:

```bash
python --version
```

**Expected output:**
```
Python 3.10.x or higher
```

If you see Python 2.x or an error, install Python 3 from [python.org](https://www.python.org/downloads/)

### Step 2: Navigate to Project Directory

```bash
cd "C:\Users\Saisr\Desktop\Coding\Algorand Playground\Algorand-Playground"
```

Or on Linux/Mac:
```bash
cd /path/to/Algorand-Playground
```

### Step 3: (Recommended) Create Virtual Environment

A virtual environment keeps dependencies isolated:

**Windows:**
```bash
python -m venv algorand-env
algorand-env\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv algorand-env
source algorand-env/bin/activate
```

You'll see `(algorand-env)` in your prompt when activated.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `py-algorand-sdk` - Official Algorand Python SDK
- `pyteal` - Smart contract development framework
- `python-dotenv` - Environment variable management
- `colorama` - Terminal color support (optional)

**Expected output:**
```
Successfully installed py-algorand-sdk-2.x.x pyteal-0.24.x python-dotenv-1.0.x
```

### Step 5: Verify Installation

Test that everything is installed correctly:

```bash
python -c "import algosdk; import pyteal; print('✓ All dependencies installed!')"
```

**Expected output:**
```
✓ All dependencies installed!
```

### Step 6: Test Blockchain Connection

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
--------------------------------------------------
```

✅ **If you see this, you're ready to go!**

## Verification Checklist

Run through these quick tests:

### 1. Test Helpers Module
```bash
python utils/helpers.py
```

Should display currency conversions and validation examples.

### 2. Test Indexer Connection
```bash
python utils/indexer_client.py
```

Should confirm Indexer is healthy and online.

### 3. View Smart Contract Code
```bash
python contracts/hello_world.py
```

Should display compiled TEAL code (requires pyteal).

## Common Installation Issues

### Issue: "python: command not found"

**Solution:**
- Windows: Use `py` instead of `python`
- Linux/Mac: Use `python3` instead of `python`
- Or add Python to PATH

### Issue: "pip: command not found"

**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Issue: "Permission denied" (Linux/Mac)

**Solution:**
```bash
pip install --user -r requirements.txt
```

Or use `sudo pip install` (not recommended).

### Issue: "SSL Certificate Error"

**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Issue: PyTeal import fails

**Solution:**
Make sure you installed dependencies:
```bash
pip install pyteal
```

## Environment Configuration (Optional)

The playground works out-of-the-box with public nodes, but you can customize:

### 1. Copy Environment Template
```bash
cp .env.example .env
```

### 2. Edit .env File
```
ALGOD_ADDRESS=https://testnet-api.algonode.cloud
ALGOD_TOKEN=

INDEXER_ADDRESS=https://testnet-idx.algonode.cloud
INDEXER_TOKEN=
```

**Note:** AlgoNode public nodes don't require tokens, so you can leave them empty.

### 3. Using Custom Nodes

If you have access to a PureStake or Algorand sandbox node:

```
ALGOD_ADDRESS=https://testnet-algorand.api.purestake.io/ps2
ALGOD_TOKEN=your-api-key-here

INDEXER_ADDRESS=https://testnet-algorand.api.purestake.io/idx2
INDEXER_TOKEN=your-api-key-here
```

## Updating Dependencies

To update to the latest versions:

```bash
pip install --upgrade py-algorand-sdk pyteal python-dotenv
```

Or regenerate requirements:

```bash
pip freeze > requirements_frozen.txt
```

## Troubleshooting Connection Issues

### Test 1: Check Internet Connection
```bash
ping google.com
```

### Test 2: Check Algorand TestNet Status
Visit: https://algoexplorerapi.io/

Should show current block height and status.

### Test 3: Test Different Node
Edit `.env` to try backup nodes:

```
ALGOD_ADDRESS=https://node.testnet.algoexplorerapi.io
```

### Test 4: Check Firewall
Ensure your firewall allows outbound HTTPS connections.

## Getting Help

If you encounter issues:

1. **Check Python version**: Must be 3.10+
2. **Check pip version**: `pip --version`
3. **Try virtual environment**: Isolates dependencies
4. **Check error messages**: Often self-explanatory
5. **Search documentation**: Most issues are common

## Next Steps

Once installation is complete:

1. ✅ Read **GETTING_STARTED.md** for quick start
2. ✅ Create your first account
3. ✅ Get test ALGO from dispenser
4. ✅ Run your first transaction

## Quick Command Reference

```bash
# Activate virtual environment (if using)
algorand-env\Scripts\activate  # Windows
source algorand-env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Test connection
python utils/algod_client.py

# Create account
python scripts/create_account.py

# Check balance
python scripts/check_balance.py

# Send ALGO
python scripts/send_algo.py

# Deactivate virtual environment
deactivate
```

## Installation Complete! 🎉

You're now ready to explore Algorand development!

**Next:** Read `GETTING_STARTED.md` for your first 5 minutes with Algorand.

---

**Need more help?**
- Check README.md for full documentation
- Visit https://developer.algorand.org/ for official docs
- Join Discord: https://discord.gg/algorand
