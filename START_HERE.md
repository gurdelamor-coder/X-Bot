# 🤖 X Bot - Quick Start Summary

## What You Get

A **FREE, 24/7 cloud-hosted bot** that automatically:
- ✅ Reposts tweets with 1,000+ engagement
- ✅ Likes tweets with 5,000+ likes  
- ✅ Runs every 15 minutes
- ✅ No subscriptions, no server costs
- ✅ Completely automated

---

## 3-Step Setup (15 minutes)

### 1️⃣ Get X API Keys (5 min)
Go to https://developer.twitter.com/portal and get 5 keys:
- Bearer Token
- API Key + Secret
- Access Token + Secret

### 2️⃣ Create GitHub Repo (5 min)
- Create new GitHub repository
- Upload these bot files
- Add your X API keys to GitHub Secrets

### 3️⃣ Activate (5 min)
- Enable GitHub Actions
- Click "Run workflow"
- Watch it work! 🎉

---

## Files Included

| File | Purpose |
|------|---------|
| **x_bot.py** | Main bot script (the brain) |
| **.github/workflows/x_bot.yml** | Automation config (runs every 15 min) |
| **requirements.txt** | Python dependencies |
| **processed_tweets.json** | Tracks processed tweets (no duplicates) |
| **README.md** | Complete setup guide |
| **SETUP_CHECKLIST.md** | Step-by-step checklist |
| **ARCHITECTURE.md** | Visual diagrams & how it works |
| **test_bot.sh** | Local testing script |

---

## How It Works

```
Every 15 minutes:
1. GitHub Actions wakes up ⏰
2. Runs your bot script 🤖
3. Bot checks X for high-engagement tweets 🔍
4. Reposts and likes qualifying tweets ❤️
5. Saves progress, goes back to sleep 💤
```

---

## Cost: $0/month

✅ GitHub Actions: Free (2,000 min/month for private repos, unlimited for public)  
✅ X API: Free tier (more than enough for this bot)  
✅ No credit card required  
✅ No hidden fees  

---

## Need Help?

📖 **Full Guide:** Read `README.md`  
✅ **Quick Start:** Read `SETUP_CHECKLIST.md`  
🏗️ **How It Works:** Read `ARCHITECTURE.md`  

---

## Customization

**Change thresholds** in `x_bot.py`:
```python
MIN_CLICKS = 1000  # Your custom value
MIN_LIKES = 5000   # Your custom value
```

**Change frequency** in `.github/workflows/x_bot.yml`:
```yaml
- cron: '*/15 * * * *'  # Every 15 minutes
- cron: '*/10 * * * *'  # Every 10 minutes
- cron: '0 * * * *'     # Every hour
```

---

## What Happens After Setup

1. Bot runs automatically every 15 minutes
2. You'll see activity in GitHub Actions tab
3. Your X account will repost/like high-engagement tweets
4. No maintenance required!

---

## Monitor Your Bot

Go to your GitHub repo → **Actions** tab

You'll see logs like:
```
✓ Reposted tweet: 1234567890
✓ Liked tweet: 9876543210
Bot completed: 2 actions taken
```

---

## Ready to Start?

1. Open `SETUP_CHECKLIST.md` for step-by-step instructions
2. Follow the checklist (takes ~15 minutes)
3. Watch your bot run automatically! 🚀

**That's it!** Your bot is now working 24/7 in the cloud, completely free.
