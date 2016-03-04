# The mongo client
from logging import getLogger
import mongo_utils as mongo

import shopaholic_analyzer

# ------------------------------------------ Globals
# Logger
g_module_logger = getLogger('analyzer.main')


# ------------------------------------------ Functions
def analyze():
	while True:
		shopaholic_analyzer.analyze()


# ------------------------------------------ Main
def main():
	# Create DB
	g_module_logger.info("Analyzer starting...")
	mongo.init_db()
	g_module_logger.info("DB initialized, start analyzing...")
	analyze()


if __name__ == "__main__":
	main()
