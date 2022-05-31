from conf.settings import MONGODB
import pymongo

""" MongoDB
    Database name: clients_database
    collection name: clients_collection """


class databaseClient:
    mongodburl = MONGODB

    def __init__(self):
        self.db= pymongo.MongoClient(self.mongodburl).clients_database.clients_collection

    def addTelegramClient(self, chat_id):
        clientAlreadyExist = self.db.find_one({"chat_id": chat_id})
        if(clientAlreadyExist):
            return False
        clientAdded = self.db.insert_one({"chat_id": chat_id}).inserted_id
        return True

    def removeTelegramClient(self, chat_id):
        self.db.delete_one({"chat_id": chat_id})
        return True

    def getAllClients(self):
        clients = self.db.find({})
        return clients
