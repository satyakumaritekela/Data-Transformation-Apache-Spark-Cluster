import requests
import csv
import json
import re
import fileConverter

# Authorization Key
Authorization_Key = {'Authorization': 'a41eae4d71ff4208be38488c39dcf880'}

# URl for retrieving the data
News_URL = 'https://newsapi.org/v2/everything'

# Keywords that needs to extract the data that are sent as a parameters in the URL
parameters = {'q': '((Canada) OR (University) OR (Dalhousie University) OR (Halifax) OR (Canada Education) OR (Moncton) OR (Toronto))', 'language': 'en',
                      'sortBy': 'relevancy', 'pageSize': 100}

# retrieving the response for the given parameters
response = requests.get(url = News_URL, headers = Authorization_Key, params = parameters)

# encoding to JSON Objects
response_string = json.dumps(response.json())
json_Response = json.loads(response_string)

# creating the article list json
articles_list = json_Response['articles']

# initializing articles data
articles_data = []

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

# iterating through the response loop for filtering the emoticons,symbols and other map symbols
for article in articles_list:
    # if author and content is none enter NAN
    if article['author'] is None:
        article['author'] = 'NAN'
    if article['author'] == "":
        article['author'] = 'NAN'
    if article['content'] is None:
        article['content'] = 'NAN'
    if article['content'] == "":
        article['content'] = 'NAN'
    # append all the articles data
    articles_data.append({
        'Author': clear_Patterns(article['author']),
        'Title': clear_Patterns(article['title']),
        'Content': clear_Patterns(article['content']),
        'Date': clear_Patterns(article['publishedAt']) 
    })

# write the data into the json file
with open('news.json', 'w') as jsonFile:
    json_formatted_articles_data = json.dumps(articles_data)
    json.dump(json.loads(json_formatted_articles_data), jsonFile, indent=4, sort_keys=True)

# converting json to txt and cav format
fileConverter.changeToText("news.json", "news.csv", "news.txt")

