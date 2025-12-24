# ✅ Setup Checklist - X Bot

Follow this checklist to get your bot running in 15 minutes:

## □ Step 1: Get X API Credentials (5 min)
- [ ] Go to https://developer.twitter.com/en/portal/dashboard
- [ ] Create a Project and App
- [ ] Set app permissions to "Read and Write"
- [ ] Generate and save 5 keys:
  - [ ] Bearer Token
  - [ ] API Key (Consumer Key)
  - [ ] API Secret (Consumer Secret)
  - [ ] Access Token
  - [ ] Access Token Secret

## □ Step 2: Create GitHub Repository (2 min)
- [ ] Go to https://github.com/new
- [ ] Create new repo (public or private)
- [ ] Don't initialize with README

## □ Step 3: Add Secrets to GitHub (3 min)
- [ ] Go to repo Settings → Secrets → Actions
- [ ] Add these 5 secrets:
  - [ ] X_BEARER_TOKEN
  - [ ] X_API_KEY
  - [ ] X_API_SECRET
  - [ ] X_ACCESS_TOKEN
  - [ ] X_ACCESS_SECRET

## □ Step 4: Upload Bot Files (3 min)
- [ ] Download all bot files
- [ ] Push to your GitHub repository:
  ```bash
  git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
  cd YOUR_REPO
  # Copy all files here
  git add .
  git commit -m "Initial bot setup"
  git push
  ```

## □ Step 5: Enable & Test (2 min)
- [ ] Go to Actions tab in your repo
- [ ] Enable workflows if prompted
- [ ] Click "Run workflow" to test immediately
- [ ] Check logs to verify it's working

## 🎉 Done!
Your bot is now running every 15 minutes, 24/7, completely free!

---

## 📊 How to Monitor

**Check bot activity:**
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click on any workflow run
4. View logs to see what tweets were processed

**What you'll see in logs:**
```
=============================================================
X Bot Running - 2024-01-15 10:30:00
=============================================================

Fetching tweets from timeline...
Searching for trending tweets...
Total tweets found: 42

High-engagement tweet found!
  ID: 1234567890
  Likes: 5,234
  Retweets: 892
  Replies: 145

✓ Reposted tweet: 1234567890
✓ Liked tweet: 1234567890

=============================================================
Bot completed: 2 actions taken
=============================================================
```

---

## ⚙️ Customization Options

**Change thresholds** (edit `x_bot.py`):
```python
MIN_CLICKS = 1000  # Change this number
MIN_LIKES = 5000   # Change this number
```

**Change frequency** (edit `.github/workflows/x_bot.yml`):
```yaml
# Every 10 minutes:
- cron: '*/10 * * * *'

# Every 30 minutes:
- cron: '*/30 * * * *'

# Every hour:
- cron: '0 * * * *'
```

---

## 🆘 Troubleshooting

**Bot not running?**
- Verify all 5 secrets are added correctly in GitHub
- Check that X app has "Read and Write" permissions
- Look at error logs in Actions tab

**No tweets being found?**
- Follow more accounts on X
- Wait a few hours for more activity
- Lower the thresholds temporarily to test

**API errors?**
- Regenerate X API tokens
- Update the secrets in GitHub
- Make sure you're not over rate limits

---

**Need help?** Check the full README.md for detailed instructions!
