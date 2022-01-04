import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd

#https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/#:~:text=Sentiment%20analysis%20is%20basically%20the,positive%20or%20negative%20or%20neutral.&text=Subjective%20sentences%20generally%20refer%20to,objective%20refers%20to%20factual%20information.


class SentimentAnalyser():
    def __init__(self, loader="en_core_web_sm"):
        print("Loading NLP Pipeline...")
        self._nlp = spacy.load(loader)
        self._nlp.add_pipe('spacytextblob')
        print("Done...")

    ## polarity is the score of negativity or positivty and subjectivity is the score of factualness or opinion (high being opinion)
    def get_sentiment(self, text):
        doc = self._nlp(text)
        return {
            "polarity": doc._.polarity,
            "subjectivity": doc._.subjectivity
        }
    
    @staticmethod
    def _sentiments_to_df(sentiments):
        return pd.DataFrame(sentiments)

    @staticmethod
    def _average_polarity(df):
        return df['polarity'].mean()
    
    @staticmethod
    def _average_subjectivity(df):
        return df['subjectivity'].mean()


    def get_average_sentiment(self, list_of_blobs=[]):
        sentiments = []
        for text in list_of_blobs:
            sentiments.append(self.get_sentiment(text))
        df = self._sentiments_to_df(sentiments)
        return {
            'polarity_average': self._average_polarity(df),
            'subjectivity_average': self._average_subjectivity(df)
        }


if __name__ == "__main__":
    text= """$BTC - We are at a place where I could see us going either way but for now my plan is UP. Whether it's a quick dip to take out longs then up, or we finally break here, this is what I'm planning for. Spot buys (no leverage cause of possible wick), and will see how this goes."""
    sentimentAnalyser = SentimentAnalyser()
    sentiment = sentimentAnalyser.get_sentiment(text)

