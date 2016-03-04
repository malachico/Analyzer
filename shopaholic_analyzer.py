from __future__ import division
import mongo_utils as mongo


def calculate_apps_score(user_id):
	pass


def calculate_gps_score(user_id):
	# Get the user's docs from GpsInfo collection
	docs_to_analyze = mongo.get_user_docs_from_collection(user_id, "GpsInfo")

	# extract the places types
	only_places_types = map(lambda doc: doc['types'], docs_to_analyze)

	# flatten all the lists of place types
	flatten_places_types = [place_type for sublist in only_places_types for place_type in sublist]

	# Get num of stores
	n_stores = len(filter(lambda place_type: "store" in place_type, flatten_places_types))

	# Get num of all places
	n_all_places = len(flatten_places_types)

	# return the ratio between the shopping places to all places
	return n_stores / n_all_places


def analyze():
	mongo.init_mongo_client()
	user_ids = mongo.get_user_ids()
	for user_id in user_ids:
		gps_score = calculate_gps_score(user_id)
		apps_score = calculate_apps_score(user_id)
