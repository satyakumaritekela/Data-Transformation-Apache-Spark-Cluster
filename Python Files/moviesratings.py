import requests
import csv
import json
import re
import fileConverter

# Authorization Key
Authorization_Key = "c14d71f2"

# URl for retrieving the data
Movies_URL = 'http://www.omdbapi.com/?apikey=c14d71f2&s='
Ratings_URL = 'http://www.omdbapi.com/?apikey=c14d71f2&t='

# Keywords that needs to extract the data that are sent as a parameters in the URL
movie_KeyWords = ["Canada", "University", "Moncton", "Halifax", "Toronto", "Vancouver", "Alberta", "Niagara"]

# initializing movies data
movies_data = []
     
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

# retrieving all the responses for the keywords
# iterating through the response loop for filtering the emoticons,symbols and other map symbols
for key in movie_KeyWords:
    response = requests.get(Movies_URL + key)
    response_string = json.dumps(response.json()['Search'])
    movie_list = json.loads(response_string)
    
    for movie in movie_list:
        movie_response = requests.get(Ratings_URL + movie['Title'])
        response_string1 = json.dumps(movie_response.json())
        movie = json.loads(response_string1)
    
        # if author and content is none enter NAN
        if movie['Title'] is None:
            movie['Title'] = 'NAN'
        if movie['imdbRating'] is None:
            movie['imdbRating'] = 'NAN'
        if movie['Genre'] is None:
            movie['Genre'] = 'NAN'
        if movie['Plot'] is None:
            movie['Plot'] = 'NAN'
            
        # append all the movies data
        movies_data.append({
            'Title': clear_Patterns(movie['Title']),
            'Genre': clear_Patterns(movie['Genre']),
            'Plot': clear_Patterns(movie['Plot']),
            'Ratings': movie['imdbRating']
        })


# write the data into the json file
with open('moviesratings.json', 'w') as jsonFile:
    json_formatted_movies_data = json.dumps(movies_data)
    json.dump(json.loads(json_formatted_movies_data), jsonFile, indent=4, sort_keys=True)
    
# converting json to txt and cav format
fileConverter.changeToText("moviesratings.json", "moviesratings.csv", "moviesratings.txt")
   
