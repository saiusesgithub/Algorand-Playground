# ⚡ Quick Start - Unified Vercel Deployment

## 🎯 One-Command Deployment

```bash
# From project root
vercel --prod
```

That's it! Everything deploys together! 🚀

---

## 📦 What Gets Deployed

✅ **React Frontend** (`frontend/`)
✅ **Python API Functions** (`api/`)
✅ **Shared Utilities** (`utils/`)

**All on one Vercel URL!**

---

## 🚀 Step-by-Step First Time Setup

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### 2. Install Vercel CLI
```bash
npm install -g vercel
```

### 3. Login to Vercel
```bash
vercel login
```

### 4. Deploy!
```bash
vercel --prod
```

---

## 🧪 Test Locally (Optional)

### Option A: Vercel Dev (Recommended)
```bash
# Runs frontend + Python functions locally
vercel dev
```

### Option B: Frontend Only
```bash
cd frontend
npm run dev
```
(API functions won't work in this mode)

---

## 📊 After Deployment

You'll get a URL like:
```
https://algorand-playground-xyz.vercel.app
```

**Test these:**
- ✅ Dashboard loads
- ✅ Network status shows "Connected"
- ✅ Create Account works
- ✅ All features functional

---

## 🔧 Build Manually (If Needed)

```bash
cd frontend
npm run build
```

Dist will be in `frontend/dist/`

---

## 📁 Project Structure

```
/
├── api/           # Python serverless functions
├── frontend/      # React app
├── utils/         # Python utilities (used by api/)
├── scripts/       # Original CLI tools
└── vercel.json    # Deployment config
```

---

## 🐛 Troubleshooting

**Issue:** Build fails
```bash
# Test build locally first
cd frontend
npm run build
```

**Issue:** API doesn't work
- Check `vercel.json` exists at root
- Verify `requirements.txt` has `py-algorand-sdk`

**Issue:** 404 errors
- Make sure deploying from project ROOT
- API files must be in `/api` directory

---

## 🌟 Why This Is Better

✅ **One deployment** (not frontend + backend separately)
✅ **One URL** (not two different hosts)
✅ **No CORS** (same domain)
✅ **Simpler** (perfect for assignments!)

---

## 🎉 That's It!

```bash
vercel --prod
```

**Boom! You're live! 🚀**
