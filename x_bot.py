#!/usr/bin/env python3
"""
X (Twitter) Bot - Repost/Like high-engagement tweets
Runs on GitHub Actions (free, 24/7)
Optimized for X Free API tier
"""

import tweepy
import os
import json
from datetime import datetime
import time

# Configuration
MIN_CLICKS = 1000  # Minimum clicks/impressions
MIN_LIKES = 5000   # Minimum likes
CHECK_PERIOD_HOURS = 24  # How far back to check

class XBot:
    def __init__(self):
        """Initialize bot with API credentials from environment variables"""
        # X API v2 credentials
        self.bearer_token = os.environ.get('X_BEARER_TOKEN')
        
        # X API v1.1 credentials (needed for posting)
        self.api_key = os.environ.get('X_API_KEY')
        self.api_secret = os.environ.get('X_API_SECRET')
        self.access_token = os.environ.get('X_ACCESS_TOKEN')
        self.access_secret = os.environ.get('X_ACCESS_SECRET')
        
        # Initialize clients
        self.client_v2 = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret,
            wait_on_rate_limit=True
        )
        
        # Load processed tweets to avoid duplicates
        self.processed_file = 'processed_tweets.json'
        self.processed_tweets = self.load_processed_tweets()
    
    def load_processed_tweets(self):
        """Load list of already processed tweet IDs"""
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_processed_tweets(self):
        """Save processed tweet IDs"""
        with open(self.processed_file, 'w') as f:
            json.dump(list(self.processed_tweets), f)
    
    def search_vira
