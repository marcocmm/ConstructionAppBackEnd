
from flask import Flask
from flask_pymongo import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://admin:admPass@constructionappcluster.qfh8l.mongodb.net/constructionDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('constructionDB')
user_collection = pymongo.collection.Collection(db, 'user')
equipment_collection = pymongo.collection.Collection(db, 'equipment')
user_type_collection = pymongo.collection.Collection(db, 'users_type')
permission_collection = pymongo.collection.Collection(db, 'permission')
provider_collection = pymongo.collection.Collection(db, 'provider')
material_collection = pymongo.collection.Collection(db, 'material')
service_collection = pymongo.collection.Collection(db, 'service')
client_collection = pymongo.collection.Collection(db, 'client')
attendance_collection = pymongo.collection.Collection(db, 'attendance')