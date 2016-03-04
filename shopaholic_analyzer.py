from __future__ import division
import mongo_utils as mongo

g_shopping_apps = ['ebay', 'amazon', 'aliexpress', 'zap', 'dealextreme', 'groupon', 'yad2', 'wish', 'you', 'chinabuy',
					'etsy', 'asos', 'bigdeal']


def calculate_apps_score(user_id):
	# Get the user's docs from AppsData collection
	docs_to_analyze = mongo.get_user_docs_from_collection(user_id, "AppsData")

	# extract the Apps
	only_apps = map(lambda doc: doc['apps'], docs_to_analyze)

	# flatten all the lists of apps
	flatten_apps = set([app for sublist in only_apps for app in sublist])

	# Get num of shopping apps
	n_shopping_apps = len(filter(lambda app: app in g_shopping_apps, flatten_apps))

	# Get num of all apps
	n_all_apps = len(flatten_apps)

	# Return the ratio between the shopping places to all places
	try:
		return n_shopping_apps / n_all_apps
	except:
		# In case n_all_apps == 0
		return 0

def calculate_gps_score(user_id):
	# Get the user's docs from GpsInfo collection
	docs_to_analyze = mongo.get_user_docs_from_collection(user_id, "GpsInfo")

	# Extract the places types
	only_places_types = map(lambda doc: doc['types'], docs_to_analyze)

	# Flatten all the lists of place types
	flatten_places_types = [place_type for sublist in only_places_types for place_type in sublist]

	# Get num of stores
	n_stores = len(filter(lambda place_type: "store" in place_type, flatten_places_types))

	# Get num of all places
	n_all_places = len(flatten_places_types)

	# return the ratio between the shopping places to all places
	try:
		return n_stores / n_all_places
	except:
		# In case the n_all_plcaces == 0
		return 0


def analyze():
	mongo.init_mongo_client()
	user_ids = mongo.get_user_ids()
	for user_id in user_ids:
		gps_score = calculate_gps_score(user_id)
		apps_score = calculate_apps_score(user_id)
		total_score = 0.3 * apps_score + 0.7 * gps_score
		mongo.update_rank(user_id, "shopaholic", total_score)
