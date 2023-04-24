"""
A Twitter bot written in Python using Tweepy. 
It will like and/or retweet tweets that contain single or multiple keywords and hashtags.
"""

# Built-in/Generic Imports
import os
import logging
from time import sleep

# Library Imports
import tweepy


import tweepy
import logging
from credentials import *

logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()



# Own modules
#from config import *

#search_keywords = "%22animal crossing%22celeste"

search_keywords = "%22nueva zelanda"

# Time to wait between processing a request in seconds 
# Information about TwitterAPI limits here: https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
delay = 10

# Specify what type of search results you want to get
# 'recent', 'popular', or 'mixed'
result_type = 'mixed'

# Specify the number of tweets you want the bot to iterate through
number_of_tweets = 500000
# OR change run_continuously to True if you want it to run continuously (or for deploying)
# if True, number_of_tweets will not be used
run_continuously = True

# Change booleans depending on if you want to only retweet, only like, or do both
retweet_tweets = True
like_tweets = True


def create_api():
    '''
SECTION FOR CONFIG / AND AUTH.

---

    '''
    consumerKey = "ENTER IT"
    consumerSecret = "ENTER IT"
    accessToken = "ENTER IT"
    accessTokenSecret = "ENTER IT"

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    #api = tweepy.API(auth, wait_on_rate_limit=True)
    api = tweepy.API(auth, wait_on_rate_limit=True)
#, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error('Authentication Error', exc_info=True)
        raise e
    logger.info(f"Authentication OK. Connected to @{api.get_user(screen_name='USERNAME HERE')}")

    return api









__author__ = 'Felipe Alfonso Gonzalez'
__version__ = '1.1.0'
__maintainer__ = 'Felipe Alfonso Gonzalez'
__email__ = 'felipe@freeshell.de'
__status__ = 'Dev'


logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

def initialize_api():
    api = create_api()
    return api

def get_tweets(api):
    # Exclude retweets from search to avoid repeats
    if run_continuously:
        tweets = tweepy.Cursor(api.search_tweets,
                        q=search_keywords + " -filter:retweets", 
                        count=100,
                        result_type=result_type,
                        monitor_rate_limit=True, 
                        wait_on_rate_limit=True,
                        lang="en").items()
    else:
        tweets = tweepy.Cursor(api.search_tweets,
                        q=search_keywords + " -filter:retweets",
                        count=100,
                        result_type=result_type,
                        monitor_rate_limit=True, 
                        wait_on_rate_limit=True,
                        lang="en").items(number_of_tweets)
    return tweets

def process_tweets(api, tweets):
    for tweet in tweets:
        tweet = api.get_status(tweet.id)
        logger.info(f"Processing tweet: {tweet.text}")

        # Ignore tweet if it is from myself or if it is a reply to a tweet
        if tweet.user.id != api.get_user(screen_name='USERNAME HERE').id or tweet.in_reply_to_status_id is not None:

            if retweet_tweets:
                if not tweet.retweeted:
                    try:
                        tweet.retweet()
                        logger.info("Retweeted now")
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        raise e
                else:
                    logger.info("Has been retweeted previously")

            if like_tweets:    
                if not tweet.favorited:
                    try:
                        tweet.favorite()
                        logger.info("Favorited now")
                    except Exception as e:
                        logger.error("Error on favorite", exc_info=True)
                        raise e
                else:
                    logger.info("Has been favorited previously")

        # Delay in between processing tweets
        sleep(delay)


if __name__ == "__main__":
    api = initialize_api()
    tweets = get_tweets(api)
    process_tweets(api, tweets)
