from pymongo import MongoClient

DB_NAME = "VendorDB"
COLLECTION_NAME = "MetaData"

MONGO_IP_INDEX = 0
MONGO_PORT_INDEX = 1

class DBManager:
    def __init__(self,db_info):
        print("opening db connection --->  ",end="")
        self.mongo_ip = db_info[MONGO_IP_INDEX]
        self.mongo_port = MONGO_PORT_INDEX
        self.mongo_client = MongoClient() #connecting to the mongo service
        self.db = self.mongo_client[DB_NAME] #creating new data base named VendorDB
        self.coll = self.db[COLLECTION_NAME] # creating new collection named MetaData
        print("db connection established")

    def __del__(self):
        self.mongo_client.close() #closing the mongo service connection
        print("closing db connection...")

    #this function organizes the list into a json format data
    def pack_metadata(self,metadata):
        keys = ["Brand","Model","Stock Rom","Android Version","Author","Name","url"]
        data = {keys[i]:metadata[i] for i in range(len(keys))}
        return data

    #inserts the data into the data base
    def insert(self,metadata):
        data = self.pack_metadata(metadata)
        self.coll.insert_one(data)

