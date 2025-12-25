import os
import json
import time
from datetime import datetime

# Your Twitter API setup here
# ...

def load_processed_tweets():
    """Load the list of already processed tweet IDs"""
    try:
        with open('processed_tweets.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_processed_tweets(tweet_ids):
    """Save the list of processed tweet IDs"""
    with open('processed_tweets.json', 'w') as f:
        json.dump(tweet_ids, f)

def main():
    processed_tweets = load_processed_tweets()
    
    try:
        # Get tweets from your target account
        # IMPORTANT: Only fetch a small number of tweets per run
        tweets = get_recent_tweets(max_results=10)  # Don't fetch 100s at once
        
        new_processed = []
        
        for tweet in tweets:
            if tweet['id'] in processed_tweets:
                continue  # Skip already processed tweets
            
            try:
                # Repost
                repost_tweet(tweet['id'])
                time.sleep(2)  # Small delay between actions
                
                # Like
                like_tweet(tweet['id'])
                time.sleep(2)
                
                new_processed.append(tweet['id'])
                print(f"✓ Processed tweet {tweet['id']}")
                
            except RateLimitError as e:
                print(f"Rate limit hit: {e}")
                print("Stopping this run. Will continue in next scheduled run.")
                break  # EXIT IMMEDIATELY - Don't sleep!
            
            except Exception as e:
                print(f"Error processing tweet {tweet['id']}: {e}")
                continue
        
        # Save progress
        all_processed = processed_tweets + new_processed
        # Keep only last 1000 to prevent file from growing forever
        save_processed_tweets(all_processed[-1000:])
        
        print(f"✓ Processed {len(new_processed)} new tweets")
        
    except RateLimitError as e:
        print(f"Rate limit hit during fetch: {e}")
        print("Will retry in next scheduled run.")
        return  # EXIT IMMEDIATELY - Don't sleep!
    
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
