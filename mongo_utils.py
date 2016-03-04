# Mongo client
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
	g_mongo_client = pymongo.MongoClient()

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
	collections = ["GpsInfo", "AppsInfo"]

	capped_collections = []

	# For each name create collection in the @g_db
	map(lambda collection_name: generate_collection(collection_name, capped=False), collections)
	map(lambda collection_name: generate_collection(collection_name, capped=True), capped_collections)


def init_db():
	init_mongo_client()
	generate_collections()


# Return all user ids in the system
def get_user_ids():
	user_ids_docs = list(g_db["users"].find({}, {"user_id": True, "_id": False}))
	return map(lambda doc: doc["user_id"], user_ids_docs)


def get_user_docs_from_collection(user_id, collection):
	return list(g_db[collection].find({"userId": user_id}))


def update_rank(user_id, index, score):
	g_db["ranks"].update({"userId": user_id},{index: score}, upsert=True)