# Mongo client
import time
from logging import getLogger

import pymongo

# ------------------------ Globals
# Logger
g_module_logger = getLogger('analyzer.main')
# DB client
g_mongo_client = None
# DB
g_db = None


# ----------------------- Functions
# initialize the mongo client
def init_mongo_client():
	global g_mongo_client, g_db
	g_mongo_client = pymongo.MongoClient("mongodb://mot:mot@ds039165.mongolab.com:39165/mirror")

	g_db = g_mongo_client['mirror']


# Return all user ids in the system
def get_user_ids():
	user_ids_docs = list(g_db["user"].find({}, {"_id": True}))
	return map(lambda doc: str(doc["_id"]), user_ids_docs)


def get_user_docs_from_collection(user_id, collection):
	return list(g_db[collection].find({"userId": user_id}))


def update_rank(user_id, index, score):
	doc_to_insert = {
		"queryId": index,
		"userId": user_id,
		"rank": score,
		"date": time.time(),
		"feedback": -1
	}
	g_db["QueryResult"].insert(doc_to_insert)
