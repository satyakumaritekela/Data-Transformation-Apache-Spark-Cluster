import sys
from pyspark import SparkContext, SparkConf
import re
import string
import pymongo
from pymongo import MongoClient

# creating spark context for the application
config = SparkConf().setAppName('Word_Count').setMaster('spark://ip-172-31-38-143.ec2.internal:7077')
sc = SparkContext(conf = config)

# mongo db connection
mongodb_connection = MongoClient('localhost', 27017)

# get mongo db
db = mongodb_connection.dmdw

# get the news and tweets data
news_data = db.news.find()
tweets_data = db.tweets.find()

# search keywords
keywords = ['education', 'canada', 'university', 'dalhousie', 'expensive', 'good school', 'good schools', 'bad school', 'bad schools', 'poor school', 'poor schools', 'faculty', 'computer science', 'graduate']

# function that converts text to lowercase and removing punctuations
def clear_patterns(ip_text):
    encoded_str = ip_text.encode('utf-8')
    lowercased_str = encoded_str.lower()
    lowercased_str = lowercased_str.replace('--',' ')
    op_str = lowercased_str.translate(None, string.punctuation)
    return op_str

# function that zips the two words to search
def zip_words(ip_text):
    return [a + " " + b for a, b in zip(ip_text.split(), ip_text.split()[1:])]

# function that updates the list
def update_list():
    # update the total list
    for keyword in keywords:
        if news_single_words.get(keyword) is None:
            news_single_words.update({keyword : 0})
        if tweets_single_words.get(keyword) is None:
            tweets_single_words.update({keyword: 0})
        if news_double_words.get(keyword) is None:
            news_double_words.update({keyword : 0})
        if tweets_double_words.get(keyword) is None:
            tweets_double_words.update({keyword:0})

# fucntion that calculates the word count   
def word_count(ip_file_name):

    # reading the data that are single
    single_word = sc.textFile(ip_file_name).flatMap(lambda line: clear_patterns(line).split(" "))
    
    # count the occurrence of single word in the text
    single_wordCount = single_word.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
    
    # single words are converted into dictionary
    single_word_dictionary = single_wordCount.collectAsMap()
    
    # reading the data that are double word
    double_word = sc.textFile(ip_file_name).flatMap(zip_words)
    
    # count the occurrence of double word in the text
    double_wordCount = double_word.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
    
    # double words are converted into dictionary
    double_word_dictionary = double_wordCount.collectAsMap()
    
    word_dictionary = []
    
    word_dictionary.append(single_word_dictionary)
    word_dictionary.append(double_word_dictionary)
    
    return word_dictionary

# word count in the news.txt
news_dictionary_list = word_count("news.txt")
news_single_words = news_dictionary_list[0]
news_double_words = news_dictionary_list[1] 

# word count in the tweets.txt
tweets_dictionary_list = word_count("tweets.txt")
tweets_single_words = tweets_dictionary_list[0]
tweets_double_words = tweets_dictionary_list[1] 

update_list()
            
#Writing the output word count to text file
word_count_data = "Word and its count from the stored data\n\n"

for keyword in keywords:
    if(('' in keyword) == True):
        word_count_data = word_count_data + keyword + " : " + str(news_double_words.get(keyword) + tweets_double_words.get(keyword)) + "\n"
    else:        
        word_count_data = word_count_data + keyword + " : " + str(news_single_words.get(keyword) + tweets_single_words.get(keyword)) + "\n"
        
print(word_count_data)
                    
# save the counts to output
with open('wordoutput.txt', 'w') as opfile:
    opfile.write(word_count_data)
    