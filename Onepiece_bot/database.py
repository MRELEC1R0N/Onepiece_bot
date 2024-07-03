
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Settings import Mongodb_api
uri = Mongodb_api

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
databasename = client['Onepiece']
users = databasename['Users']
crew = databasename['crew']
islands = databasename['islands']
