import os
import tweepy
import json
import time

class TwitterSearcher():
    def __init__(self, _API_KEY, _API_KEY_SECRET, _BEARER_TOKEN):
        self._API_KEY = _API_KEY
        self._API_KEY_SECRET = _API_KEY_SECRET
        self._BEARER_TOKEN = _BEARER_TOKEN
        auth = tweepy.AppAuthHandler(self._API_KEY, self._API_KEY_SECRET)
        self.api = tweepy.API(auth)  

        # In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.

    @staticmethod
    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.errors.TooManyRequests:
                print(f"Rate Limited Reached for Twitter Bot, Sleeping...")
                time.sleep(15 * 60)
            except StopIteration:
                return
                

    def _get_symbol_tweets(self, symbol, limit=1000):
        tweets = list()
        for tweet in self.limit_handled(tweepy.Cursor(self.api.search_tweets, q=f"${symbol}").items(limit)):
        # for tweet in tweepy.Cursor(self.api.search_tweets, q=f"${symbol}").items(limit):
            tweets.append(tweet.text)
        print(f"Enumerated {limit} tweets for {symbol}...")    
        return tweets
    
    def find_symbols_tweets(self, symbols, limit=1000):
        symbol_tweets = dict()
        for symbol in symbols:
            symbol_tweets[symbol] = self._get_symbol_tweets(symbol, limit)
        return symbol_tweets
        

    
if __name__ == "__main__":
    twit = TwitterSearcher()
    tweets = twit.find_symbols_tweets(["BTC", "ETH"])
    print(tweets)
