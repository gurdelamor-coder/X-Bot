#!/usr/bin/env python3
"""
X (Twitter) Bot - Repost/Like high-engagement tweets
Runs on GitHub Actions (free, 24/7)
"""

import tweepy
import os
import json
from datetime import datetime, timedelta

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
    
    def get_timeline_tweets(self):
        """Fetch tweets from home timeline"""
        try:
            # Get authenticated user's ID
            me = self.client_v2.get_me()
            user_id = me.data.id
            
            # Fetch home timeline
            tweets = self.client_v2.get_home_timeline(
                max_results=100,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                exclude=['retweets', 'replies']
            )
            
            return tweets.data if tweets.data else []
        except Exception as e:
            print(f"Error fetching timeline: {e}")
            return []
    
    def search_trending_tweets(self):
        """Search for trending tweets (alternative method)"""
        try:
            # Search recent tweets with high engagement
            query = "-is:retweet -is:reply has:media"
            tweets = self.client_v2.search_recent_tweets(
                query=query,
                max_results=100,
                tweet_fields=['public_metrics', 'created_at', 'author_id'],
                sort_order='relevancy'
            )
            
            return tweets.data if tweets.data else []
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []
    
    def meets_criteria(self, tweet):
        """Check if tweet meets engagement criteria"""
        metrics = tweet.public_metrics
        
        # Note: X API may not provide "impression_count" in free tier
        # We'll use available metrics: retweet_count, reply_count, like_count, quote_count
        
        likes = metrics.get('like_count', 0)
        # Estimate clicks/impressions from engagement (rough approximation)
        total_engagement = (
            metrics.get('retweet_count', 0) + 
            metrics.get('reply_count', 0) + 
            metrics.get('like_count', 0) + 
            metrics.get('quote_count', 0)
        )
        
        # Check criteria
        meets_like_threshold = likes >= MIN_LIKES
        meets_engagement_threshold = total_engagement >= MIN_CLICKS / 10  # Rough estimate
        
        return meets_like_threshold or meets_engagement_threshold
    
    def repost_tweet(self, tweet_id):
        """Repost (retweet) a tweet"""
        try:
            self.client_v2.retweet(tweet_id)
            print(f"✓ Reposted tweet: {tweet_id}")
            return True
        except Exception as e:
            print(f"✗ Error reposting {tweet_id}: {e}")
            return False
    
    def like_tweet(self, tweet_id):
        """Like a tweet"""
        try:
            self.client_v2.like(tweet_id)
            print(f"✓ Liked tweet: {tweet_id}")
            return True
        except Exception as e:
            print(f"✗ Error liking {tweet_id}: {e}")
            return False
    
    def run(self):
        """Main bot logic"""
        print(f"\n{'='*60}")
        print(f"X Bot Running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Fetch tweets
        print("Fetching tweets from timeline...")
        timeline_tweets = self.get_timeline_tweets()
        
        print("Searching for trending tweets...")
        trending_tweets = self.search_trending_tweets()
        
        all_tweets = timeline_tweets + trending_tweets
        print(f"Total tweets found: {len(all_tweets)}\n")
        
        # Process tweets
        actions_taken = 0
        for tweet in all_tweets:
            tweet_id = tweet.id
            
            # Skip if already processed
            if str(tweet_id) in self.processed_tweets:
                continue
            
            # Check if meets criteria
            if self.meets_criteria(tweet):
                metrics = tweet.public_metrics
                print(f"\nHigh-engagement tweet found!")
                print(f"  ID: {tweet_id}")
                print(f"  Likes: {metrics.get('like_count', 0)}")
                print(f"  Retweets: {metrics.get('retweet_count', 0)}")
                print(f"  Replies: {metrics.get('reply_count', 0)}")
                
                # Repost and like
                if self.repost_tweet(tweet_id):
                    actions_taken += 1
                
                if self.like_tweet(tweet_id):
                    actions_taken += 1
                
                # Mark as processed
                self.processed_tweets.add(str(tweet_id))
        
        # Save processed tweets
        self.save_processed_tweets()
        
        print(f"\n{'='*60}")
        print(f"Bot completed: {actions_taken} actions taken")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    bot = XBot()
    bot.run()
