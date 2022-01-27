from pymongo import MongoClient
from uuid import uuid4
import requests
from datetime import datetime
import json
from dotenv import dotenv_values

class Database:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.db = MongoClient(self.config["MONGOURL"]).StudyBudy
        self.users = self.db.users
        
    def addUser(self, email):
        user = {
            "_id": str(uuid4()),
            "email": email,
            "name": email.split("@")[0],
            "boards": [],
        }
        self.users.insert_one(user)
    
    def getUserByEmail(self, email):
        return self.users.find_one({"email": email})
    
    def getUser(self, id):
        return self.users.find_one({"_id": id})
    
    def userExists(self, email):
        return self.users.find_one({"email": email}) is not None
    
    def getBoards(self, id):
        return self.users.find_one({"_id": id})["boards"]