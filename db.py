
from flask import Flask
from flask_pymongo import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://admin:admPass@constructionappcluster.qfh8l.mongodb.net/constructionDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('constructionDB')
user_collection = pymongo.collection.Collection(db, 'users')