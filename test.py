# import random

# with open ("daily_tweets.txt", "r") as daily_tweets_file:
#     daily_tweets = daily_tweets_file.readlines()
#     daily_tweets = [s.rstrip("\n") for s in daily_tweets]
#     random.shuffle(daily_tweets)

# with open ("daily_tweets.txt", "w") as daily_tweets_file:
#     for item in daily_tweets:
#         daily_tweets_file.write(item + "\n")

import logging
import time
from datetime import datetime


class Bot:
    """Create the bot"""
    def __init__(self):
        self.daily_index = 0

    def post_daily_tweet(self):
        # Import all daily_tweets from the 'daily_tweets.txt' into a list without the '\n' character
        with open ("daily_tweets.txt", "r") as daily_tweets_file:
            daily_tweets = daily_tweets_file.readlines()
            daily_tweets = [s.rstrip("\n") for s in daily_tweets]
            logging.debug("daily_tweets.txt loaded")

        # Get a message from the list of messages wrote.
        daily_tweet = daily_tweets[self.daily_index]
        self.daily_index += 1
        logging.debug("found random daily_tweet")
        logging.info(daily_tweet)
        print(daily_tweet)
        if self.daily_index == len(daily_tweets) :
            print("\n\n\n")
            self.daily_index = 0
        

            
    def run(self):
        """Run the main loop."""
        while True:
            self.post_daily_tweet()


            time.sleep(0.1)
if __name__ == "__main__":
    """Launch the bot when running the program.""" 
    Bot().run()
