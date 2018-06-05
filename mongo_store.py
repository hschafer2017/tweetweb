from tweepy import Stream
from tweepy.streaming import StreamListener
from auth import get_auth
from pymongo import MongoClient
import json

MONGODB_URI = "mongodb://brian-haley:pa55word@ds247310.mlab.com:47310/bglynch-twitter"

MONGODB_NAME = "bglynch-twitter"

def mongo_store(q):
    class MyStreamListener(StreamListener):
        # Class that Tweepy has built, has collects all functionality of tweets
    
        def __init__(self):
            super(MyStreamListener, self).__init__()
            self.num_tweets = 0
    
        def on_data(self, data):
            if self.num_tweets < 10:
                self.num_tweets += 1
                try:
                    with MongoClient(MONGODB_URI) as conn:
                        db = conn[MONGODB_NAME]
                        coll = db[q]
                        coll.insert(json.loads(data))
                        return True
                except BaseException as e:
                    print ("Failed on_data: %s" % str(e))
                    return True
            else:
                return False
    
        def on_error(self, status):
            print(status)
            return True
        auth = get_auth()
        twitter_stream = Stream(auth, MyStreamListener())
        twitter_stream.filter(track=q)