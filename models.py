from pymongo import MongoClient
from uuid import uuid4
import requests
from datetime import datetime
import json
from dotenv import dotenv_values
import random

class Database:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.db = MongoClient(self.config["MONGOURL"]).StudyBudy
        self.users = self.db.users
        self.boards = self.db.boards
        
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
        boards = []
        for board in self.users.find_one({"_id": id})["boards"]:
            boards.append(self.boards.find_one({"_id": board}))
        return boards

    def addBoard(self, name, id):
        data = {
            "_id": str(uuid4()),
            "name": name,
            "color": "#" + "".join([random.choice("0123456789ABCDEF") for i in range(6)]),
            "tasks": {},
            "columns": {},
            "columnOrder": [],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.boards.insert_one(data)
        self.users.update_one({"_id": id}, {"$push": {"boards": data["_id"]}}, upsert=True)
    
    def getBoard(self, id, user_id):
        board = self.boards.find_one({"_id": id})
        # return board
        user = self.users.find_one({"_id": user_id})
        if id in user["boards"]:
            return board
        return None