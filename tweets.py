import tweepy
from auth import get_api

api = get_api()


def search(query, count):
    return [status for status in tweepy.Cursor(api.search, q=query).items(count)]
    
tweets = search("Trump", 10)

for tweet in tweets: 
    print("Profile Picture: " + tweet.user.profile_image_url_https)
    print("Username: @" + tweet.user.screen_name)
    print("Text: " + tweet.text)
    hashtags = [h.text for h in tweet.entities['hashtags']]
    print("Hashtags: " + str(hashtags))
    print("Favorites: " + str(tweet.favorite_count))
    print("Retweets: " + str(tweet.retweet_count))
    print("Followers: " + str(tweet.user.followers_count))
    print("Following: " + str(tweet.user.friends_count))
    print("Number of Tweets: " + str(tweet.user.statuses_count))
