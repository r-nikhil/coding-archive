
# import logging
# from twitter_bot import TwitterBot
# from utils.tweet_analyzer import analyze_tweets

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def test_meme_replies():
#     try:
#         # Initialize bot
#         logger.info("Initializing Twitter bot...")
#         bot = TwitterBot()
        
#         # Get all accounts from file
#         try:
#             with open('twitter_accounts.txt', 'r') as f:
#                 accounts = [acc.strip() for acc in f.read().strip().split(',') if acc.strip()]
#         except Exception as e:
#             logger.error(f"Error reading twitter_accounts.txt: {str(e)}")
#             accounts = ["manasjsaloi"]  # Fallback
            
#         for account in accounts:
#             try:
#                 # Fetch tweets for each account
#                 logger.info(f"Fetching tweets from @{account}")
#                 tweets = bot.fetch_tweets(account, limit=5)
                
#                 if not tweets:
#                     logger.error(f"No tweets found for @{account}")
#                     continue
                    
#                 # Analyze and get top tweet
#                 logger.info(f"Analyzing tweets for @{account}...")
#                 analyzed_tweets = analyze_tweets(tweets)
#                 if not analyzed_tweets:
#                     logger.error(f"Failed to analyze tweets for @{account}")
#                     continue
                    
#                 top_tweet = analyzed_tweets[0]
                
#                 logger.info(f"Selected top tweet for @{account}:")
#                 logger.info(f"Tweet ID: {top_tweet.get('id', 'N/A')}")
#                 logger.info(f"Username: {top_tweet.get('username', 'N/A')}")
#                 logger.info(f"Text: {top_tweet.get('text', 'N/A')}")
#                 logger.info(f"Engagement score: {top_tweet.get('engagement_score', 'N/A')}")
                
#                 # Generate meme text
#                 logger.info("Preparing text for meme generation...")
#                 meme_text = top_tweet['text']
#                 if len(meme_text) > 300:
#                     logger.info("Text exceeds 300 characters, will be summarized...")
                
#                 # Try to post meme reply
#                 logger.info(f"Attempting to post meme reply for @{account}...")
#                 try:
#                     success = bot.post_reply_with_meme(top_tweet)
                    
#                     if success:
#                         logger.info(f"Successfully posted meme reply to @{account}!")
#                     else:
#                         logger.error(f"Failed to post meme reply to @{account} - check Twitter bot logs")
#                 except Exception as reply_error:
#                     logger.error(f"Error during meme reply to @{account}: {str(reply_error)}")
                    
#             except Exception as acc_error:
#                 logger.error(f"Error processing account @{account}: {str(acc_error)}")
#                 continue
            
#     except Exception as e:
#         logger.error(f"Test failed: {str(e)}")
#         logger.exception("Full stack trace:")

# if __name__ == "__main__":
#     test_meme_replies()
