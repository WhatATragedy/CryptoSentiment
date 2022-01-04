## Sentiment Analysis Explained Simply 

Sentiment Analysis is basically the practice of finding out how positive, or negative a body of text is.
There are two values being spit out here, polarity_average and subjectivity average.

## How to Use
Unfortunately I've not done a command line interface, or actually made this ready to use for anyone other than myself. More work needed to make this viable over time!
```
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
```

### ToDo
- [x] Add DB to look at mean sentiment over time
- [ ] Add CLI
- [ ] Add other sources to scrape

### Polarity Average
Typically we quanitfy the sentiment of that positivty and negativity as a value called polarity. The overall sentiment is often inferred as positive, neutral or negative from the sign of the polarity score.
Polarity scores range from -1 to 1. -1 being very negative, and 1 being positive.


### Subjectivity Average
Subjectivity is the score of factualness or opinion, a high score on the scale of -1 to 1 means opinion, -1 is factual.

#### * More reading to be done 
https://realpython.com/sentiment-analysis-python/#classifying-reviews

