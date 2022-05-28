from conf.settings import MONGODB
import pymongo

""" MongoDB
    Database name: client
    collection name: clients """

class databaseClient:
    mongodburl = MONGODB

    def __init__(self):
        self.client = pymongo.MongoClient(self.mongodburl)
        self.db = self.client.clients_database.clients_collection

    def addTelegramClient(self, chat_id):
        clientAlreadyExist = self.db.find_one({"chat_id": chat_id})
        if(clientAlreadyExist): return False
        clientAdded = self.db.insert_one({"chat_id": chat_id}).inserted_id
        return True
    
    def removeTelegramClient(self, chat_id):
        try:
            self.db.delete_one({"chat_id": chat_id})
            return True
        except: return False
    
    def getAllClients(self):
        clients = self.db.find({})
        return clients
