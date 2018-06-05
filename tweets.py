import tweepy
from auth import get_api

api = get_api()


def search(query, count):
    return [{'text':status.text, 'id':status.id} for status in tweepy.Cursor(api.search, q=query).items(count)]

# code for testing    
# tweets = search("Trump", 10)
# for tweet in tweets: 
#     print(tweet)
