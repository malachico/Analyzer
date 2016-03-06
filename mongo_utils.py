# Mongo client
from datetime import time
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


def generate_collection(collection_name, capped):
	try:
		if capped:
			g_mongo_client.sf.create_collection(collection_name,
			                                    capped=True,
			                                    size=1 * 1024 * 1024 * 1024,
			                                    max=500000)
		else:
			g_mongo_client.sf.create_collection(collection_name)

	except (pymongo.errors.CollectionInvalid, pymongo.errors.OperationFailure):
		pass


def generate_collections():
	collections = ["users", "GpsInfo", "AppsInfo", "query-result"]

	capped_collections = []

	# For each name create collection in the @g_db
	map(lambda collection_name: generate_collection(collection_name, capped=False), collections)
	map(lambda collection_name: generate_collection(collection_name, capped=True), capped_collections)


def generate_indexes():
	g_db["query-result"].create_index(("userId", pymongo.ASCENDING), unique=True)


def init_db():
	init_mongo_client()
	generate_collections()
	generate_indexes()


# Return all user ids in the system
def get_user_ids():
	user_ids_docs = list(g_db["users"].find({}, {"userId": True, "_id": False}))
	return map(lambda doc: doc["userId"], user_ids_docs)


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
	g_db["query-result"].insert(doc_to_insert)
