#!/usr/bin/env python3
"""
X Bot - Simple version that works with X Free API
"""

import tweepy
import os
import json
from datetime import datetime
import time

MIN_LIKES = 5000

class XBot:
    def __init__(self):
        self.bearer_token = os.environ.get('X_BEARER_TOKEN')
        self.api_key = os.environ.get('X_API_KEY')
        self.api_secret = os.environ.get('X_API_SECRET')
        self.access_token = os.environ.get('X_ACCESS_TOKEN')
        self.access_secret = os.environ.get('X_ACCESS_SECRET')
        
        self.client_v2 = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret,
            wait_on_rate_limit=True
        )
        
        self.processed_file = 'processed_tweets.json'
        self.processed_tweets = self.load_processed_tweets()
    
    def load_processed_tweets(self):
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_processed_tweets(self):
        with open(self.processed_file, 'w') as f:
            json.dump(list(self.processed_tweets), f)
    
    def get_timeline_tweets(self):
        """Get tweets from accounts you follow"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            
            tweets = self.client_v2.get_home_timeline(
                max_results=50,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                exclude=['retweets', 'replies']
            )
            
            return tweets.data if tweets.data else []
        except Exception as e:
            print(f"Error fetching timeline: {e}")
            return []
    
    def search_tweets(self):
        """Search for tweets - simplified for Free API"""
        try:
            # Simple query that works with Free API
            tweets = self.client_v2.search_recent_tweets(
                query="python",
                max_results=10,
                tweet_fields=['public_metrics', 'created_at', 'author_id']
            )
            return tweets.data if tweets.data else []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def meets_criteria(self, tweet):
        """Check if tweet has enough engagement"""
        try:
            metrics = tweet.public_metrics
            likes = metrics.get('like_count', 0)
            return likes >= MIN_LIKES
        except:
            return False
    
    def repost_tweet(self, tweet_id):
        """Retweet a tweet"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            self.client_v2.retweet(tweet_id, user_id=user_id)
            print(f"✓ Reposted: {tweet_id}")
            return True
        except Exception as e:
            print(f"✗ Repost failed: {e}")
            return False
    
    def like_tweet(self, tweet_id):
        """Like a tweet"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            self.client_v2.like(tweet_id, user_id=user_id)
            print(f"✓ Liked: {tweet_id}")
            return True
        except Exception as e:
            print(f"✗ Like failed: {e}")
            return False
    
    def run(self):
        print(f"\n{'='*60}")
        print(f"X Bot Running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Try timeline first
        print("Checking timeline...")
        tweets = self.get_timeline_tweets()
        
        # If timeline is empty, try search
        if not tweets:
            print("Timeline empty. Trying search...")
            tweets = self.search_tweets()
        
        print(f"Found {len(tweets)} tweets\n")
        
        actions =
