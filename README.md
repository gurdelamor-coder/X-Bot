# X (Twitter) Bot - Complete Setup Guide

## 🎯 What This Bot Does
- Runs 24/7 in the cloud (FREE using GitHub Actions)
- Automatically reposts tweets with 1,000+ clicks/engagement
- Automatically likes tweets with 5,000+ likes
- No subscriptions, no server costs

## 🚀 Setup Instructions (15 minutes)

### Step 1: Get X (Twitter) API Credentials

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Sign in with your X account
3. Click "Create Project" (if you don't have one)
4. Create an App inside the project
5. Go to your App's "Keys and Tokens" tab
6. Generate and save these credentials:
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
   - **Bearer Token**
   - **Access Token**
   - **Access Token Secret**

**Important:** Set your app permissions to "Read and Write" in the App settings!

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (can be private or public)
3. Name it something like "x-bot" or "twitter-bot"
4. Don't initialize with README (we'll push our files)

### Step 3: Add API Keys to GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of these:

   | Secret Name | Value |
   |------------|--------|
   | `X_BEARER_TOKEN` | Your Bearer Token |
   | `X_API_KEY` | Your API Key |
   | `X_API_SECRET` | Your API Secret |
   | `X_ACCESS_TOKEN` | Your Access Token |
   | `X_ACCESS_SECRET` | Your Access Token Secret |

### Step 4: Push Bot Files to GitHub

Open your terminal and run these commands:

```bash
# Clone your empty repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Copy all bot files into this directory
# (Copy: x_bot.py, requirements.txt, processed_tweets.json, and the .github folder)

# Initialize git and push
git add .
git commit -m "Initial bot setup"
git branch -M main
git push -u origin main
```

### Step 5: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. If prompted, click "I understand my workflows, go ahead and enable them"
4. You should see "X Bot - Auto Repost & Like" workflow

### Step 6: Activate the Bot

The bot will now run automatically every 15 minutes!

To test it immediately:
1. Go to **Actions** tab
2. Click "X Bot - Auto Repost & Like"
3. Click **Run workflow** → **Run workflow**
4. Wait 30 seconds and refresh to see the results

## 📊 Monitoring Your Bot

### Check Bot Activity
1. Go to **Actions** tab in your repository
2. Click on any workflow run to see logs
3. You'll see which tweets were reposted/liked

### View Statistics
The logs show:
- Number of tweets checked
- Tweets that met criteria
- Actions taken (reposts/likes)
- Any errors

## ⚙️ Configuration

Edit `x_bot.py` to customize:

```python
MIN_CLICKS = 1000  # Minimum engagement threshold
MIN_LIKES = 5000   # Minimum likes threshold
```

Edit `.github/workflows/x_bot.yml` to change frequency:

```yaml
# Current: Every 15 minutes
- cron: '*/15 * * * *'

# Every 10 minutes:
- cron: '*/10 * * * *'

# Every 30 minutes:
- cron: '*/30 * * * *'

# Every hour:
- cron: '0 * * * *'
```

## 🔄 How It Works

1. **GitHub Actions** triggers the workflow every 15 minutes
2. Bot fetches tweets from your timeline and trending tweets
3. Checks each tweet's engagement metrics:
   - Likes count
   - Total engagement (likes + retweets + replies + quotes)
4. If criteria met → repost and like
5. Saves processed tweet IDs to avoid duplicates
6. Commits the updated list back to repository

## 💰 Cost Breakdown

| Service | Cost | Usage |
|---------|------|-------|
| X API (Free Tier) | $0 | Basic access |
| GitHub Actions | $0 | 2,000 min/month (private) or unlimited (public) |
| **Total** | **$0/month** | ✅ Completely free |

**Note:** For private repos, 2,000 minutes = ~133 hours of runtime, which is more than enough for this bot running a few seconds every 15 minutes.

## 🛠️ Troubleshooting

### Bot Not Running
- Check GitHub Actions tab for error messages
- Verify all 5 secrets are added correctly
- Make sure your X app has "Read and Write" permissions

### API Rate Limits
- X Free tier: 1,500 tweets read per month
- Bot automatically waits when hitting rate limits
- Reduce frequency if needed

### No Tweets Found
- Bot searches your timeline and trending tweets
- Follow more accounts to get more tweets in timeline
- The search function looks for recent high-engagement tweets

### Authentication Errors
- Regenerate your X API tokens
- Update the secrets in GitHub
- Ensure app permissions are set to "Read and Write"

## 🎓 Advanced Tips

### Run on Multiple Accounts
1. Create separate repositories for each account
2. Use different X API credentials for each
3. Each runs independently

### Customize Search Criteria
Edit the `search_trending_tweets()` function:
```python
# Current search
query = "-is:retweet -is:reply has:media"

# Search specific topics
query = "python -is:retweet -is:reply"

# Search specific language
query = "-is:retweet -is:reply lang:en"
```

### Add Filtering
Add keywords to avoid:
```python
BLOCKED_WORDS = ['spam', 'scam', 'crypto']

def should_process(tweet):
    text = tweet.text.lower()
    return not any(word in text for word in BLOCKED_WORDS)
```

## 📝 File Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── x_bot.yml          # GitHub Actions config
├── x_bot.py                   # Main bot script
├── requirements.txt           # Python dependencies
├── processed_tweets.json      # Tracks processed tweets
└── README.md                  # This guide
```

## 🔒 Security Notes

- Never commit API keys to the repository
- Always use GitHub Secrets for credentials
- Keep your repository private if you prefer
- Regularly rotate your API tokens

## 📈 Expected Results

- **Runs:** Every 15 minutes = 96 times per day
- **Actions:** Depends on your timeline activity
- **API Usage:** Well within free tier limits
- **Uptime:** 24/7/365 (as long as GitHub Actions is running)

## ⏰ Keeping It Running

GitHub Actions workflows automatically stay active unless:
- Repository is deleted
- Workflow is manually disabled
- No commits for 60 days (to reactivate: just make any commit)

To ensure it stays active, you can:
1. Make a dummy commit monthly, OR
2. Set up a separate workflow to auto-commit monthly

## 🎉 You're Done!

Your bot is now running 24/7 in the cloud, completely free! Check the Actions tab regularly to monitor its activity.

---

**Questions or Issues?** Check the Actions logs for detailed error messages.
