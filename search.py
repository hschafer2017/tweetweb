import os
from tweets import search
from flask import Flask, redirect, render_template, request
from tweepy import Stream
from tweepy.streaming import StreamListener
from auth import get_auth
from pymongo import MongoClient
import json
import tweepy
from tweepy import OAuthHandler

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME')

app = Flask(__name__)

@app.route('/')
def get_homepage():
   return render_template("index.html")

@app.route('/new_search')
def get_results_page():
    q = request.args.get('search')
    tweets = search(q, 10)
    
#Mongo Database
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


    return render_template("results.html", tweets = tweets, q = q)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug = True)