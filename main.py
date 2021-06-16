import argparse
import logging
import os
import random
import sys
import time
from datetime import datetime

import twitter
from dotenv import load_dotenv

# Import the dotenv file.
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Accessing keys in the dotenv file.
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token_key = os.getenv("ACCESS_TOKEN_KEY")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Accessing twitter user id in the dotenv file.
# To get a twitter id check : https://codeofaninja.com/tools/find-twitter-id/
user_id = os.getenv("USER_ID")
screen_name = os.getenv("SCREEN_NAME")

# Add argument to increase output verbosity
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

parser.add_argument("-d", "--debug", help="increase output verbosity to debug mode",
                    action="store_true")

args = parser.parse_args()

# Print help for arguments needed
if len(sys.argv) > 0 and (sys.argv[0] == "-h" or sys.argv[0] == "--help"):
    parser.print_help()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

if args.verbose :
    logging.basicConfig(level=logging.INFO)


class Bot:
    """Create the bot"""
    def __init__(self):
        """Initialize the bot."""
        logging.info(f"Initializing the bot at {datetime.now()}")
        self.api = self.get_config()
        self.last_tweet = None  # Value to stock the last tweet posted
        self.tweet = None  # Value to stock the actual tweet posted 
        self.daily_index = 0
        
        # Import all messages from the 'messages.txt' into a list without the '\n' character
        with open ("messages.txt", "r") as self.love_msg_file:
            tmp = self.love_msg_file.readlines()
            self.love_msg = [tweet_status.rstrip("\n") for tweet_status in tmp]
            logging.debug("messages.txt loaded")
        
        # Get the last tweet from the target user.
        tweets = self.api.GetUserTimeline(user_id = user_id, screen_name = screen_name, include_rts = False, exclude_replies = True, since_id= 0, count = 1)
        if tweets:
            self.tweet = tweets[0]
            logging.info("got user Timeline")

        # Store the last tweet posted when the bot starts.
        if self.tweet and not self.last_tweet:
            self.last_tweet = self.tweet
            logging.debug("Last tweet stored")
        
        logging.info("Bot initialized")

    def get_config(self):
        """Get the Twitter API."""
        logging.info("Getting API config")
        return twitter.Api(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret)

    def post_daily_tweet(self):
        """Get Current time"""
        today = datetime.now()

        # If it's 18:00pm.
        if ((f"{today.hour}:{today.minute}") == "18:0") and today.second <= 10:
            logging.info("tweeting daily status")
            # Import all daily_tweets from the 'daily_tweets.txt' into a list without the '\n' character
            with open ("daily_tweets.txt", "r") as daily_tweets_file:
                daily_tweets = daily_tweets_file.readlines()
                daily_tweets = [s.rstrip("\n") for s in daily_tweets]
                logging.debug("daily_tweets.txt loaded")

            # Get a message from the list of messages wrote.
            daily_tweet = daily_tweets[self.daily_index]
            self.daily_index
            logging.debug("found random daily_tweet")
            logging.info(daily_tweet)
            if self.daily_index == len(daily_tweets)-1 :
                self.daily_index = 0

            try:
                self.api.PostUpdate(daily_tweet)
                logging.info("Daily tweet posted")
                time.sleep(10)
            except logging.error as e:
                with open ("logs.log", "a") as logfile:
                    logfile.write(f"[{datetime.now().upper}]: ERROR POSTUPDATE FOR DAILY STATUS {e}")
                    logging.debug("ERROR POSTUPDATE FOR DAILY STATUS")
                pass

    def run(self):
        """Run the main loop."""
        logging.info("Bot running")
        while True:
            logging.debug("Start loop")
            # Tweet a daily status
            self.post_daily_tweet()

            # Get the last tweet from the target user.
            tweets = self.api.GetUserTimeline(user_id = user_id, screen_name = screen_name, include_rts = False, exclude_replies = True, since_id= 0, count = 1)
            if tweets:
                self.tweet = tweets[0]
                print(self.tweet)
                logging.info("got user Timeline")
                logging.debug(self.tweet.text)

            # When a new tweet is posted, initialize the values.
            if (self.tweet and not self.last_tweet) or ((self.tweet and self.last_tweet) and self.last_tweet.text != self.tweet.text):
                logging.info("user posted a tweet")
                self.last_tweet = self.tweet

                # Get a rancom index in the list
                random_index = random.randint(0, len(self.love_msg) - 1)

                # Get a random message from the list of messages wrote.
                message = self.love_msg[random_index]

                # String of the @user.
                tag = f"@{self.tweet.user.screen_name} "

                # Post a comment under last user's tweet. Comment = '@user message'
                try:
                    self.api.PostUpdate(tag + message , in_reply_to_status_id = self.tweet.id)
                    logging.info("Reply posted")
                    time.sleep(5)
                except logging.error as e:
                    with open ("logs.log", "a") as logfile:
                        logfile.write(f"[{datetime.now().upper}]: ERROR POSTUPDATE FOR REPLY {e}")
                        logging.debug("ERROR POSTUPDATE FOR REPLY")
                    continue

            time.sleep(5)

if __name__ == "__main__":
    """Launch the bot when running the program.""" 
    Bot().run()
