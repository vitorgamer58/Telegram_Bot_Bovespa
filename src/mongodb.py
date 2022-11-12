from conf.settings import MONGODB
from operator import itemgetter
import pymongo

""" MongoDB
    Database name: clients_database
    collection name: clients_collection """


class databaseClient:
    mongodburl = MONGODB

    def __init__(self):
        self.db = pymongo.MongoClient(
            self.mongodburl).clients_database.clients_collection

    def addTelegramClient(self, chat):
        id, username, first_name = itemgetter(
            'id', 'username', 'first_name')(chat)
        clientAlreadyExist = self.db.find_one({"chat_id": id})
        if(clientAlreadyExist):
            return False
        self.db.insert_one({
            "first_name": first_name,
            "username": username,
            "chat_id": id
        })
        return True

    def removeTelegramClient(self, chat_id):
        self.db.delete_one({"chat_id": chat_id})
        return True

    def getAllClients(self):
        clients = self.db.find({})
        return clients
