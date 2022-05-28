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

    def addTelegramClient(self, chatId):
        clientAlreadyExist = self.db.find_one({"chatId": chatId})
        if(clientAlreadyExist): return False
        clientAdded = self.db.insert_one({"chatId": chatId}).inserted_id
        return True
    
    def removeTelegramClient(self, chatId):
        try:
            self.db.delete_one({"chatId": chatId})
            return True
        except: return False

