import json
from CoinMarketCap import CoinMarketCap
from TwitterBot import TwitterSearcher
from sentiment import SentimentAnalyser
import pandas as pd
import datetime
from dataclasses import dataclass, asdict
from db import DBUtil

@dataclass
class Crypto:
    ticker: str
    polarity: float
    subjectivity: float
    rank: int
    date: datetime.datetime

if __name__ == "__main__":
    environment_file = ".env.json"
    with open(environment_file) as config:
        config_data = json.load(config)
        TWIT_API_KEY = config_data.get('API_KEY')
        TWIT_API_KEY_SECRET = config_data.get('API_KEY_SECRET')
        TWIT_BEARER_TOKEN = config_data.get('BEARER_TOKEN')
        CMC_API_KEY = config_data.get("CMC_API_KEY")
    

    cmc = CoinMarketCap(api_key=CMC_API_KEY)
    data = cmc.get_listings(return_limit=20, direction="front")
    symbols = cmc.get_symbols_and_rank(data)
    # symbols is a dict of ticker = cmc_rank

    print(f"About to enumerate [{len(symbols.keys())}] Assets...")
    twit = TwitterSearcher(TWIT_API_KEY, TWIT_API_KEY_SECRET, TWIT_BEARER_TOKEN)
    tweets = twit.find_symbols_tweets(symbols.keys(), limit=500)
    #tweets will be a dict with the symbol as the key and the tweets a list of values
    sentimentAnalyser = SentimentAnalyser()
    crypto_sentiment = list()
    for symbol in tweets.keys():
        sentiment = sentimentAnalyser.get_average_sentiment(tweets.get(symbol))
        analysed_symbol = Crypto(
            symbol,
            sentiment.get("polarity_average"),
            sentiment.get("subjectivity_average"),
            symbols.get(symbol),
            datetime.date.today()
        )
        crypto_sentiment.append(analysed_symbol)
    df = pd.DataFrame.from_records([s.__dict__ for s in crypto_sentiment])
    db = DBUtil()
    # db.create_table()
    db.upload_items_batch(crypto_sentiment)
