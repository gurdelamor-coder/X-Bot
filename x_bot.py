#!/usr/bin/env python3
"""
X Bot - Simple version that works with X Free API
"""
import tweepy
import os
import json
from datetime import datetime
import time

# Adjusted thresholds for more activity
MIN_LIKES_FOR_REPOST = 50  # Lower threshold for reposting
MIN_LIKES_FOR_LIKE = 50      # Even lower threshold for just liking

class XBot:
    def __init__(self):
        self.bearer_token = os.environ.get('X_BEARER_TOKEN')
        self.api_key = os.environ.get('X_API_KEY')
        self.api_secret = os.environ.get('X_API_SECRET')
        self.access_token = os.environ.get('X_ACCESS_TOKEN')
        self.access_secret = os.environ.get('X_ACCESS_SECRET')
        
        # FIXED: Set wait_on_rate_limit=False so script exits instead of sleeping
        self.client_v2 = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret,
            wait_on_rate_limit=False  # CRITICAL FIX
        )
        
        self.processed_file = 'processed_tweets.json'
        self.processed_tweets = self.load_processed_tweets()
        
        # Top verified followers (usernames)
        self.top_followers = [
            'KameronBennett', 'BBGreatMoments', 'MikeWellsAuthor', 
            'GoodAmerica1', 'JossSheldon', 'TheJudge96',
            'chloe4djt', 'obeyguy', 'mil_vet17', 'Godfatherparte2',
            '7MohammedKhaled', 'WickedDog3', 'Brookltnwilliw', 
            'AntoniusCDN', 'urara326', 'SilverInstitute',
            'SimanjuntakElly', 'KozyKeyleth', 'RichardCarthon', 'LoveFromManali'
        ]
    
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
        except tweepy.TooManyRequests as e:
            print(f"Rate limit hit on timeline fetch. Exiting.")
            return []
        except Exception as e:
            print(f"Error fetching timeline: {e}")
            return []
    
    def search_tweets(self):
        """Search for tweets - FIXED for Free API"""
        try:
            # Strategy 1: Search tweets from top verified followers
            print("Searching tweets from top verified followers...")
            
            # Build query for top 5 followers (to avoid query length limits)
            follower_query = " OR ".join([f"from:{username}" for username in self.top_followers[:5]])
            query = f"({follower_query}) -is:retweet -is:reply"
            
            tweets = self.client_v2.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['public_metrics', 'created_at', 'author_id']
            )
            
            result_tweets = tweets.data if tweets.data else []
            
            # Strategy 2: If no results, try general trending topics
            if not result_tweets:
                print("No tweets from followers, trying trending topics...")
                trending_queries = [
                    "cryptocurrency -is:retweet -is:reply",
                    "AI technology -is:retweet -is:reply",
                    "blockchain -is:retweet -is:reply"
                ]
                
                for trending_query in trending_queries:
                    try:
                        tweets = self.client_v2.search_recent_tweets(
                            query=trending_query,
                            max_results=10,
                            tweet_fields=['public_metrics', 'created_at', 'author_id']
                        )
                        if tweets.data:
                            result_tweets.extend(tweets.data)
                            break
                    except tweepy.TooManyRequests:
                        print(f"Rate limit hit on search. Exiting.")
                        return result_tweets
                    except Exception as e:
                        print(f"Error with query '{trending_query}': {e}")
                        continue
            
            return result_tweets
            
        except tweepy.TooManyRequests:
            print(f"Rate limit hit on search. Exiting.")
            return []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def should_like(self, tweet):
        """Check if tweet should be liked"""
        try:
            metrics = tweet.public_metrics
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            
            # Like if it has decent engagement
            return likes >= MIN_LIKES_FOR_LIKE or retweets >= 10
        except:
            return False
    
    def should_repost(self, tweet):
        """Check if tweet should be reposted (higher threshold)"""
        try:
            metrics = tweet.public_metrics
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            
            # Repost if it has significant engagement
            return likes >= MIN_LIKES_FOR_REPOST or (likes >= 500 and retweets >= 50)
        except:
            return False
    
    def repost_tweet(self, tweet_id):
        """Retweet a tweet"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            self.client_v2.retweet(tweet_id, user_id=user_id)
            print(f"  ✓ Reposted: {tweet_id}")
            return True
        except tweepy.TooManyRequests:
            print(f"  ✗ Rate limit hit on repost. Stopping.")
            return False
        except Exception as e:
            print(f"  ✗ Repost failed: {e}")
            return False
    
    def like_tweet(self, tweet_id):
        """Like a tweet"""
        try:
            me = self.client_v2.get_me()
            user_id = me.data.id
            self.client_v2.like(tweet_id, user_id=user_id)
            print(f"  ✓ Liked: {tweet_id}")
            return True
        except tweepy.TooManyRequests:
            print(f"  ✗ Rate limit hit on like. Stopping.")
            return False
        except Exception as e:
            print(f"  ✗ Like failed: {e}")
            return False
    
    def run(self):
        print(f"\n{'='*60}")
        print(f"X Bot Running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Try timeline first
        print("Fetching tweets from timeline...")
        tweets = self.get_timeline_tweets()
        
        # If timeline is empty or has few tweets, try search
        if len(tweets) < 5:
            print("Searching for trending tweets...")
            search_tweets = self.search_tweets()
            tweets.extend(search_tweets)
        
        print(f"Total tweets found: {len(tweets)}\n")
        
        actions = 0
        max_actions = 10  # Increased limit for more activity
        
        for tweet in tweets:
            if actions >= max_actions:
                print(f"\nReached max actions limit ({max_actions})")
                break
            
            tweet_id = tweet.id
            
            # Skip if already processed
            if str(tweet_id) in self.processed_tweets:
                continue
            
            # Get metrics
            metrics = tweet.public_metrics
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            
            # Check if meets any criteria
            should_like = self.should_like(tweet)
            should_repost = self.should_repost(tweet)
            
            if should_like or should_repost:
                print(f"Processing tweet {tweet_id}:")
                print(f"  Likes: {likes}, Retweets: {retweets}")
                
                # Like the tweet
                if should_like:
                    if self.like_tweet(tweet_id):
                        actions += 1
                        time.sleep(2)  # Rate limit protection
                    else:
                        # If like failed due to rate limit, stop
                        break
                
                # Repost if highly engaged
                if should_repost:
                    if self.repost_tweet(tweet_id):
                        actions += 1
                        time.sleep(2)
                    else:
                        # If repost failed due to rate limit, stop
                        break
                
                # Mark as processed
                self.processed_tweets.add(str(tweet_id))
                self.save_processed_tweets()
        
        print(f"\n{'='*60}")
        print(f"Bot completed: {actions} actions taken")
        print(f"Processed tweets total: {len(self.processed_tweets)}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    bot = XBot()
    bot.run()
