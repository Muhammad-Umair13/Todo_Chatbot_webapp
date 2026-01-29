# Quick Fix Guide: Gemini API Chatbot Issue

## 🔴 Problem Summary
Your chatbot is not working because the Gemini API key has **exceeded the free tier quota (429 error)**.

```
Current API Key: REDACTED_GEMINI_API_KEY
Status: ❌ Quota exhausted (0 remaining requests)
```

> **Security note:** Removed the literal API key from this document. Keep keys only in `backend/.env` or a secret manager and rotate the key if it was previously pushed to a public repo.

---

## 🟢 Quick Solutions (Choose One)

### Solution 1: Get a New API Key (5 min) ⭐ Quickest
If you just want to test immediately:

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key" → "Create API key in new project"
3. Copy the new key
4. Edit `backend/.env`:
   ```
   GEMINI_API_KEY=YOUR_NEW_KEY_HERE
   ```
5. Restart backend: `python -m uvicorn src.main:app --reload`
6. Test chatbot

**Note:** Still has free tier limits, but you get a fresh quota

---

### Solution 2: Upgrade to Paid Plan (10 min) ⭐ Best for Production
For permanent, reliable chatbot:

1. Go to: https://ai.google.dev/pricing
2. Click "Get API Key" → Enable billing
3. Select your project
4. Set up payment method
5. Your existing key will now work with paid tier

**Cost:** ~$0.075 per 1M input tokens (very cheap)

---

### Solution 3: Use Different AI Provider (20 min)
If you want to avoid Google APIs:

**Option A: OpenAI (GPT-3.5 Turbo)**
- Edit `backend/src/chatbot/services.py`
- Replace Gemini client with OpenAI client
- Update system prompt if needed
- Add `OPENAI_API_KEY` to `.env`

**Option B: Anthropic (Claude)**
- Similar steps as OpenAI
- More expensive but excellent for task management

---

## ✅ What's Already Fixed

### 1. Installed Missing Package
```bash
✅ google-genai>=1.0.0 (was missing)
```

### 2. Added Smart Error Handling
```python
# Routes now return helpful error messages:
- 429: "AI service quota exceeded. Please upgrade or try later."
- 500: Generic error handling
```

### 3. Better Logging
```python
# Now logs quota errors specifically
logger.error("API Quota Exceeded - Free tier limit reached")
```

### 4. Proper Error Propagation
```python
# Errors flow through: AgentService → Router → Frontend
# Frontend shows user-friendly messages
```

---

## 🧪 How to Test

### Test 1: Verify Backend is Running
```bash
curl http://localhost:8000/health
# Should return: {"status": "ok"}
```

### Test 2: Test Gemini API (requires new key)
```bash
cd backend
python test_gemini_live.py
# Will show:
# ✅ "Using API Key: AIzaS...xxxxx"
# ✅ "Sending message to Gemini..."
# ✅ Response from Gemini
```

### Test 3: Test Frontend Chatbot
1. Open frontend at http://localhost:3000
2. Click chat button (bottom right)
3. Send a message
4. Should get AI response (once API key is fixed)

---

## 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend Server | ✅ Running | Port 8000 |
| Database | ✅ Connected | Neon PostgreSQL |
| Chat Routes | ✅ Ready | `/api/chat/*` working |
| Frontend Chat UI | ✅ Ready | Waiting for API responses |
| **Gemini API** | ❌ **Needs Fix** | **Quota exhausted** |
| Error Handling | ✅ Improved | Now returns proper error codes |

---

## 🚀 Next Steps (Do This Now)

### Step 1: Get a New API Key
- Go to https://aistudio.google.com/app/apikey
- Create new API key
- Copy it

### Step 2: Update .env
```bash
cd backend
# Edit .env file
# Find: GEMINI_API_KEY=REDACTED_GEMINI_API_KEY
# Replace with: GEMINI_API_KEY=YOUR_NEW_KEY

> **Security note:** Removed literal API key to prevent accidental commits. If this key was ever pushed, rotate it immediately and consider rewriting git history.
```

### Step 3: Restart Backend
```bash
# Stop current server (Ctrl+C)
# Then restart:
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Test in Frontend
1. Open http://localhost:3000
2. Click the chat button
3. Send: "Hello, who are you?"
4. Should get response!

---

## 💡 Pro Tips

1. **Check API Usage:** Visit https://console.cloud.google.com/ to monitor quota
2. **Set Email Alerts:** Get notified before quota is reached
3. **Cache Responses:** Same user questions return cached answers
4. **Rate Limiting:** Add per-user rate limits to prevent abuse

---

## 📝 File Changes Made

### Updated Files:
1. `backend/src/chatbot/router.py`
   - Added 429 status code handling for quota exceeded
   - Better error messages for users

2. `backend/src/chatbot/services.py`
   - Added try/catch in agent.run() method
   - Logs quota errors specifically
   - Re-raises with better context

3. `backend/.env`
   - Already has GEMINI_API_KEY field (just needs new value)

### New Files:
1. `GEMINI_API_FIX.md` - Detailed technical analysis
2. This file - Quick reference guide

---

## ❓ FAQ

**Q: Will my code changes be lost?**
A: No! I improved error handling but didn't remove any features.

**Q: How long does quota reset?**
A: Free tier resets every 24 hours (or when you upgrade to paid).

**Q: Can I test without API key?**
A: No, need valid key with available quota.

**Q: Will users see the API key?**
A: No! It's only in backend `.env` file (not sent to frontend).

**Q: Cost estimate for production?**
A: ~$0.075 per 1M input tokens. A typical chat = 500 tokens = $0.00004

---

## 🆘 Still Not Working?

1. **Check backend logs:**
   ```
   Look for "Using API Key: AIzaS..." in terminal
   If not there, .env not being loaded
   ```

2. **Verify .env is in right place:**
   ```
   backend/.env  ✅ Correct
   .env          ❌ Wrong
   ```

3. **Restart after changing .env:**
   ```
   Stop server (Ctrl+C)
   python -m uvicorn src.main:app --reload
   ```

4. **Check error in browser console:**
   ```
   Press F12 → Console tab
   Look for actual error messages
   ```

---

**Time to Fix:** 5-10 minutes  
**Difficulty:** Easy  
**Testing:** Can verify immediately  

---

Need help? Check `GEMINI_API_FIX.md` for detailed technical analysis.
