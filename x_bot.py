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
    
    def search_viral_tweets(self):
        """Search for viral tweets using X API Free tier"""
        all_tweets = []
        
        # Try multiple simple search queries
        search_queries = [
            "lang:en",  # English tweets
        ]
        
        for query in search_queries:
            try:
                print(f"Searching with query: {query}")
                
                tweets = self.client_v2.search_recent_tweets(
                    query=query,
                    max_results=10,  # Small number to avoid rate limits
                    tweet_fields=['public_metrics', 'created_at', 'author_id', 'text'],
                    expansions=['author_id']
                )
                
                if tweets.data:
                    all_tweets.extend(tweets.data)
                    print(f"Found {len(tweets.data)} tweets")
                else:
                    print("No tweets found for this query")
                
                # Small delay between queries to avoid rate limits
                time.sleep(2)
                
            except tweepy.TooManyRequests as e:
                print(f"Rate limit hit. Waiting...")
                time.sleep(60)  # Wait 1 minute
            except Exception as e:
                print(f"Error searching with query '{query}': {e}")
                continue
        
        return all_tweets
    
    def meets_criteria(self, tweet):
        """Check if tweet meets engagement criteria"""
        try:
            metrics = tweet.public_metrics
            
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            replies = metrics.get('reply_count', 0)
            quotes = metrics.get('quote_count', 0)
            
            # Total engagement
            total_engagement = likes + retweets + replies + quotes
            
            # Check criteria
            meets_like_threshold = likes >= MIN_LIKES
            meets_engagement_threshold = total_engagement >= MIN_CLICKS / 10
            
            if meets_like_threshold or meets_engagement_threshold:
                print(f"Tweet meets criteria: {likes} likes, {total_engagement} total engagement")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error checking criteria: {e}")
            return False
    
    def repost_tweet(self, tweet_id):
        """Repost (retweet) a tweet"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            
            self.client_v2.retweet(tweet_id, user_id=user_id)
            print(f"✓ Reposted tweet: {tweet_id}")
            return True
        except tweepy.Forbidden as e:
            print(f"✗ Cannot repost (already retweeted or protected): {tweet_id}")
            return False
        except Exception as e:
            print(f"✗ Error reposting {tweet_id}: {e}")
            return False
    
    def like_tweet(self, tweet_id):
        """Like a tweet"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            
            self.client_v2.like(tweet_id, user_id=user_id)
            print(f"✓ Liked tweet: {tweet_id}")
            return True
        except tweepy.Forbidden as e:
            print(f"✗ Cannot like (already liked): {tweet_id}")
            return False
        except Exception as e:
            print(f"✗ Error liking {tweet_id}: {e}")
            return False
    
    def run(self):
        """Main bot logic"""
        print(f"\n{'='*60}")
        print(f"X Bot Running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Search for viral tweets
        print("Searching for viral tweets...")
        all_tweets = self.search_viral_tweets()
        
        print(f"\nTotal tweets found: {len(all_tweets)}")
        print(f"Processing tweets...\n")
        
        # Process tweets
        actions_taken = 0
        processed_count = 0
        
        for tweet in all_tweets:
            try:
                tweet_id = tweet.id
                
                # Skip if already processed
                if str(tweet_id) in self.processed_tweets:
                    print(f"⊘ Already processed: {tweet_id}")
                    continue
                
                processed_count += 1
                
                # Check if meets criteria
                if self.meets_criteria(tweet):
                    metrics = tweet.public_metrics
                    
                    print(f"\n{'='*50}")
                    print(f"🔥 High-engagement tweet found!")
                    print(f"{'='*50}")
                    print(f"ID: {tweet_id}")
                    print(f"Text: {tweet.text[:100]}...")
                    print(f"Likes: {metrics.get('like_count', 0):,}")
                    print(f"Retweets: {metrics.get('retweet_count', 0):,}")
                    print(f"Replies: {metrics.get('reply_count', 0):,}")
                    print(f"Quotes: {metrics.get('quote_count', 0):,}")
                    
                    # Repost and like
                    if self.repost_tweet(tweet_id):
                        actions_taken += 1
                    
                    # Small delay between actions
                    time.sleep(1)
                    
                    if self.like_tweet(tweet_id):
                        actions_taken += 1
                    
                    print(f"{'='*50}\n")
                else:
                    print(f"⊘ Tweet {tweet_id} doesn't meet criteria")
                
                # Mark as processed
                self.processed_tweets.add(str(tweet_id))
                
            except Exception as e:
                print(f"Error processing tweet: {e}")
                continue
        
        # Save processed tweets
        self.save_processed_tweets()
        
        print(f"\n{'='*60}")
        print(f"✅ Bot completed!")
        print(f"   Tweets checked: {processed_count}")
        print(f"   Actions taken: {actions_taken}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        bot = XBot()
        bot.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        raise
