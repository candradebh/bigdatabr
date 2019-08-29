from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

#consumer key, consumer secret, access token, access secret.

ckey="PMrkmRMQy3n7yZnBcY4GYihM6"
csecret="f3e9oFfDfw3MA8ZmrV6QbeSthUDO8UTdb3TFrOsdkGmWRmmzCx"
atoken="92998645-EphmhVfonqO2YbXtBmRIcgZSpA6aoGt6nNPD8JAI9"
asecret="0MbzoFCMq4LrGcya8ro2XMrjBifteujAa3NnVsgepHDG4"

from pymongo import MongoClient
#clienteMongo = MongoClient('192.168.82.118', 27017,username='root', password='root')




class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(tweet)


            
            #clienteMongo = MongoClient('localhost', 27017)
            #banco = clienteMongo.igti
            #sentiments = banco.sentiments
            #sentiments.insert_many([{'time':time_ms,'tweet': tweet, 'sentiment': sentiment}])
           

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)


while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["a","e","i","o","u"])
    except Exception as e:
        print(str(e))
        time.sleep(5)