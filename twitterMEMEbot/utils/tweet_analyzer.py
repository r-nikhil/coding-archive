from typing import List, Dict
from datetime import datetime
import re

def calculate_engagement_score(tweet: Dict) -> float:
    """
    Calculate engagement score based on likes, retweets, and replies
    """
    likes_weight = 1.0
    retweets_weight = 1.5
    replies_weight = 1.2
    
    score = (
        tweet['likes'] * likes_weight +
        tweet['retweets'] * retweets_weight +
        tweet['replies'] * replies_weight
    )
    
    # Normalize by time (newer tweets get slight boost)
    try:
        tweet_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    except ValueError:
        tweet_time = datetime.utcnow()  # Fallback to current time if parsing fails
    hours_ago = (datetime.utcnow() - tweet_time).total_seconds() / 3600
    time_factor = max(0.5, 1 - (hours_ago / 72))  # Decay over 3 days
    
    return score * time_factor

def analyze_sentiment(text: str) -> float:
    """
    Basic sentiment analysis using keyword matching
    """
    positive_words = {'love', 'great', 'good', 'amazing', 'awesome', 'excellent', 'happy', 'thanks', 'thank'}
    negative_words = {'bad', 'hate', 'terrible', 'awful', 'worst', 'sad', 'angry'}
    
    words = set(re.findall(r'\w+', text.lower()))
    positive_count = len(words.intersection(positive_words))
    negative_count = len(words.intersection(negative_words))
    
    return (positive_count - negative_count) * 0.1

def analyze_tweets(tweets: List[Dict]) -> List[Dict]:
    """
    Analyze tweets and return sorted by engagement score
    """
    if not tweets or not isinstance(tweets, list):
        return []
    for tweet in tweets:
        # Calculate base engagement score
        engagement_score = calculate_engagement_score(tweet)
        
        # Add sentiment bonus
        sentiment_score = analyze_sentiment(tweet['text'])
        engagement_score += sentiment_score
        
        tweet['engagement_score'] = round(engagement_score, 2)
    
    # Sort by engagement score
    sorted_tweets = sorted(tweets, key=lambda x: x['engagement_score'], reverse=True)
    return sorted_tweets
