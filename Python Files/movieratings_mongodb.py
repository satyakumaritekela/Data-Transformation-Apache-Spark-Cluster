import pymongo
import json
from pymongo import MongoClient
from pprint import pprint

# connection configurations
host_address = "@ec2-54-166-216-147.compute-1.amazonaws.com"
user_name = "satya"
password = "satya123"

# mongo db connection
try:
    mongodb_connection = pymongo.MongoClient("mongodb://" + user_name + ':' + password + host_address + ":27017/dwdm")
except Exception as e:
    print("Check MongoDB connection..")
    print(e)

# get mongo db
database = mongodb_connection.dwdm

# get the news and tweets data
movies_data = database['movies'].find()

for movie in movies_data: 
   print(movie)