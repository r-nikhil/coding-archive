from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import logging
from typing import List, Dict, Optional
import json
import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils.ai_services import AIServices

class TwitterBot:
    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        """Initialize TwitterBot with optional cookies"""
        try:
            # Initialize Chrome webdriver
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            
            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            service = ChromeService()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Initialize AI services
            self.ai_services = AIServices()
            
            # Load cookies from config if not provided
            if cookies is None:
                try:
                    with open('config.json', 'r') as f:
                        config = json.load(f)
                        cookies = config.get('twitter_cookies', {})
                except Exception as e:
                    logging.error(f"Error loading cookies from config.json: {str(e)}")
                    cookies = {}
            
            self.cookies = cookies
            if self.cookies:
                self._setup_cookies()
                
        except Exception as e:
            logging.error(f"Error initializing TwitterBot: {str(e)}")
            raise

    def __del__(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except Exception:
                pass

    def check_auth(self) -> bool:
        try:
            self.driver.get('https://x.com/x')
            return 'x.com/x' in self.driver.current_url
        except:
            return False

    def _get_user_id(self, username: str) -> str:
        try:
            self.driver.get(f'https://x.com/{username}')
            time.sleep(2)  # Wait for page load
            return self.driver.execute_script('''
                return window.__INITIAL_STATE__.entities.users.entities[Object.keys(window.__INITIAL_STATE__.entities.users.entities)[0]].id_str
            ''')
        except Exception as e:
            logging.error(f"Error getting user ID for {username}: {str(e)}")
            return None

    def _setup_cookies(self) -> None:
        """Set up cookies for authentication"""
        try:
            self.driver.get('https://x.com')
            for name, value in self.cookies.items():
                self.driver.add_cookie({'name': name, 'value': value, 'domain': '.x.com'})
        except Exception as e:
            logging.error(f"Error setting up cookies: {str(e)}")
            raise

    def fetch_tweets(self, username: str, limit: int = 20) -> List[Dict]:
        """Fetch tweets from a specific user"""
        try:
            url = f'https://x.com/{username}'
            logging.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait longer for dynamic content to load
            time.sleep(5)
            
            # Wait for tweet elements to be present
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
            except TimeoutException:
                logging.error(f"No tweets found for {username} after waiting")
                return []
            
            tweets = self.driver.execute_script('''
                const tweets = [];
                const tweetElements = document.querySelectorAll('[data-testid="tweet"]');
                
                tweetElements.forEach(tweet => {
                    try {
                        const tweetLink = tweet.querySelector('a[href*="/status/"]');
                        const tweetId = tweetLink ? tweetLink.href.split('/status/')[1] : null;
                        const textElement = tweet.querySelector('[data-testid="tweetText"]');
                        const text = textElement ? textElement.innerText : '';
                        
                        // Parse engagement metrics, handling 'K' and 'M' suffixes
                        const parseMetric = (str) => {
                            if (!str) return 0;
                            str = str.toLowerCase();
                            if (str.endsWith('k')) return parseFloat(str) * 1000;
                            if (str.endsWith('m')) return parseFloat(str) * 1000000;
                            return parseInt(str) || 0;
                        };
                        
                        const likes = parseMetric(tweet.querySelector('[data-testid="like"]')?.innerText);
                        const retweets = parseMetric(tweet.querySelector('[data-testid="retweet"]')?.innerText);
                        const replies = parseMetric(tweet.querySelector('[data-testid="reply"]')?.innerText);
                        
                        if (tweetId && text) {
                            tweets.push({
                                id: tweetId,
                                text: text,
                                likes: likes,
                                retweets: retweets,
                                replies: replies,
                                username: arguments[0],
                                created_at: new Date().toUTCString()
                            });
                        }
                    } catch (error) {
                        console.error('Error processing tweet:', error);
                    }
                });
                
                return tweets.slice(0, arguments[1]);
            ''', username, limit)
            
            if not tweets:
                logging.warning(f"No valid tweets found for {username}")
                return []
                
            logging.info(f"Successfully fetched {len(tweets)} tweets for {username}")
            return tweets
            
        except Exception as e:
            logging.error(f"Error fetching tweets for {username}: {str(e)}")
            return []

    def post_reply_with_meme(self, tweet: Dict) -> bool:
        """Post only the meme image as a reply to a tweet"""
        temp_file = 'temp_meme.png'
        try:
            logging.info(f"Posting meme reply for tweet ID: {tweet['id']}")
            
            # Get the meme URL from the tweet data (it should already be generated)
            meme_url = tweet.get('meme_url')
            if not meme_url:
                logging.error("No meme URL found in tweet data")
                return False
                
            # Download meme image with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    logging.info(f"Downloading meme from URL: {meme_url}")
                    meme_response = requests.get(meme_url, timeout=30)
                    meme_response.raise_for_status()
                    
                    with open(temp_file, 'wb') as f:
                        f.write(meme_response.content)
                    logging.info("Successfully downloaded meme image")
                    break
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        logging.error(f"Failed to download meme after {max_retries} attempts: {str(e)}")
                        return False
                    logging.warning(f"Attempt {attempt + 1} failed, retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)  # Exponential backoff
            
            # Post reply
            tweet_url = f"https://x.com/{tweet['username']}/status/{tweet['id']}"
            logging.info(f"Navigating to tweet: {tweet_url}")
            
            try:
                # Navigate and wait for page load
                self.driver.get(tweet_url)
                time.sleep(2)  # Wait for initial page load
                
                # Verify we're on the correct page
                if not tweet['id'] in self.driver.current_url:
                    logging.error("Failed to load tweet page correctly")
                    return False
                
                # Find and click reply button
                try:
                    reply_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="reply"]'))
                    )
                    reply_button.click()
                    logging.info("Clicked reply button")
                except TimeoutException:
                    logging.error("Reply button not found or not clickable")
                    return False
                
                # Upload meme image
                try:
                    file_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
                    )
                    abs_path = os.path.abspath(temp_file)
                    file_input.send_keys(abs_path)
                    logging.info("Uploaded meme image")
                    
                    # Wait for image upload to complete
                    time.sleep(2)
                except TimeoutException:
                    logging.error("File input not found")
                    return False
                
                # Add #memeBOT text to the reply
                try:
                    text_input = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
                    self.driver.execute_script("arguments[0].value = '#memeBOT';", text_input)
                    logging.info("Added #memeBOT text to reply")
                except Exception as e:
                    logging.error(f"Error adding #memeBOT text: {str(e)}")
                    return False
                
                # Submit reply
                try:
                    tweet_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]'))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", tweet_button)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", tweet_button)
                    logging.info("Clicked tweet button")
                except TimeoutException:
                    logging.error("Tweet button not found or not clickable")
                    return False
                
                # Wait for confirmation
                time.sleep(3)
                
                # Verify the reply was posted
                if "Something went wrong" in self.driver.page_source:
                    logging.error("Twitter reported an error after posting")
                    return False
                    
                logging.info("Successfully posted reply with meme")
                return True
                
            except TimeoutException as e:
                logging.error(f"Timeout while interacting with tweet page: {str(e)}")
                return False
            except WebDriverException as e:
                logging.error(f"WebDriver error: {str(e)}")
                return False
                
        except Exception as e:
            logging.error(f"Unexpected error in post_reply_with_meme: {str(e)}")
            return False
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logging.info("Cleaned up temporary meme file")
                except Exception as e:
                    logging.warning(f"Failed to remove temp file: {str(e)}")
                    pass