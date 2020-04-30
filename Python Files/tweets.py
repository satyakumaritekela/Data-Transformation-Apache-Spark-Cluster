import tweepy
import requests
import csv
import json
import re
import datetime
from unittest.test.testmock.testpatch import function
import fileConverter

# Twitter Credentials
twitter_keys = {
            'consumer_key': 'iTqwAeSi4ZbOX3SNMAPdlvouV',
            'consumer_secret': 'u70QOrP9Xrv6ZeKzlIw7aZZZB1U6xONfCXRy5bZJQd2X8JqMjn',
            'access_token': '1232333140292784128-CUSOt4mFaW0ZHVHl13bkVEQ4JRUyGb',
            'access_token_secret': 'l62oipFN72kLoOOpwbXupsg0fgZb6YEkLNGTnReaL8ZXX'
        }

# Authorization to Tweepy API
authorization = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
authorization.set_access_token(twitter_keys['access_token'], twitter_keys['access_token_secret'])
API_Reference = tweepy.API(authorization, wait_on_rate_limit = True)

# Keywords that needs to extract the data that are passed to Stream API
keyword =  ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Canada Education']
    
# pattern that filters out the emoticons,symbols and other map symbols
emojiPattern = re.compile("["
                u"\U0001F600-\U0001F64F"
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF" 
                u"\U0001F1E0-\U0001F1FF"
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)

# takes the data and clears the emoji patterns and special characters and URL's
def clear_Patterns(ip_text):
    ip_text = emojiPattern.sub(r'', ip_text)
    ip_text = " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", ip_text).split()) 
    return ip_text if ip_text != "" else "NAN"  

# initializing tweets data
tweepy_Canada = []
tweepy_University = []
tweepy_Dalhousie_University = []
tweepy_Halifax = []
tweepy_Canada_Education = []
tweets_data = []

# Stream API
# class that overrides the tweepy.streamlsitner
class StreamListner(tweepy.StreamListener):
    # constructor for storing noof tweets
    def __init__(self):
        super(StreamListner, self).__init__()
        self.noofTweets = 0
        
    def on_status(self, status):
        self.noofTweets+=1
        # Limiting for 1750 tweets
        if(self.noofTweets <= 1750): 
            # filter the text of the tweet
            try:
                status.retweeted_status.text = "RT " + clear_Patterns(status.retweeted_status.text)
                ip_text = status.retweeted_status.text
            except AttributeError:
                status.text = clear_Patterns(status.text)
                ip_text =  status.text 
                         
            # if author and content is none enter NAN
            if status.user.location == "":
                status.user.location = "NAN"
                
            # append the tweet to the tweet list
            tweets_data.append({
                'Author': status.author.screen_name,
                'Text': ip_text,
                'Location': status.user.location,
                'Date': status.created_at
            })
            return True
        else:
            return False
        
    def on_error(self, status):
        print(status)   

# creating a stream listner object
tweetsStreamListner = StreamListner()
tweetsStream = tweepy.Stream(authorization, listener = tweetsStreamListner)

# filtering the stream
tweetsStream.filter(track = keyword, languages = ["en"], is_async = True)

# function that clears the pattern and append to the json
def tweepyData(tweets):
    for tweet in tweets[0]:
        # filter the text of the tweet
        try:
            tweet.retweeted_status.full_text = "RT " + clear_Patterns(tweet.retweeted_status.full_text)
            ip_text = tweet.retweeted_status.full_text
        except AttributeError:
            tweet.full_text = clear_Patterns(tweet.full_text)
            ip_text =  tweet.full_text         
            
        # if author and content is none enter NAN
        if tweet.user.location == "":
            tweet.user.location = "NAN"
            
        # append the tweet to the tweet list
        tweets_data.append({
            'Author': tweet.user.screen_name,
            'Text': ip_text,
            'Location': clear_Patterns(tweet.user.location),
            'Date': tweet.created_at
        })

# Noof Tweets using Search API
noof_Tweets = 350

# Querying using Serach API a total of 1750 tweets using Search API
tweets_Canada = tweepy.Cursor(API_Reference.search, q = keyword[0], lang="en", tweet_mode = "extended").items(noof_Tweets)
tweepy_Canada.append(tweets_Canada)
tweepyData(tweepy_Canada)

tweets_University = tweepy.Cursor(API_Reference.search, q = keyword[1], lang="en", tweet_mode = "extended").items(noof_Tweets)
tweepy_University.append(tweets_University)
tweepyData(tweepy_University)

tweets_Dalhousie_University = tweepy.Cursor(API_Reference.search, q = keyword[2], lang="en", tweet_mode = "extended").items(noof_Tweets)
tweepy_Dalhousie_University.append(tweets_Dalhousie_University)
tweepyData(tweepy_Dalhousie_University)

tweets_Halifax = tweepy.Cursor(API_Reference.search, q = keyword[3], lang="en", tweet_mode = "extended").items(noof_Tweets)
tweepy_Halifax.append(tweets_Halifax)
tweepyData(tweepy_Halifax)

tweets_Canada_Education = tweepy.Cursor(API_Reference.search, q = keyword[4], lang="en", tweet_mode = "extended").items(noof_Tweets)
tweepy_Canada_Education.append(tweets_Canada_Education)
tweepyData(tweepy_Canada_Education)
     

# function that converts the date in date time formatter
def dateTimeConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# write the data into the json file
with open('tweets.json', 'w') as jsonFile:
    json_formatted_tweets_data = json.dumps(tweets_data, default = dateTimeConverter)
    json.dump(json.loads(json_formatted_tweets_data), jsonFile, indent=4, sort_keys=True)
    
# converting json to txt and cav format
fileConverter.changeToText("tweets.json", "tweets.csv", "tweets.txt")   
