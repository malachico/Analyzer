# The mongo client
from logging import getLogger

import time

import angriness_analyzer
import clumsiness_analyzer
import mongo_utils as mongo
import shopaholic_analyzer
import social_network_analyzer

# ------------------------------------------ Globals
# Logger
g_module_logger = getLogger('analyzer.main')


# ------------------------------------------ Functions
def analyze_all():
	shopaholic_analyzer.analyze()
	social_network_analyzer.analyze()
	clumsiness_analyzer.analyze()
	angriness_analyzer.analyze()

# ------------------------------------------ Main
def main():
	# Create DB
	g_module_logger.info("Analyzer starting...")
	mongo.init_db()
	g_module_logger.info("DB initialized, start analyzing...")
	analyze_all()


if __name__ == "__main__":
	main()
