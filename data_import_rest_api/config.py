import logging
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

# PrestaShop API Configuration
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

# Prestashop urls
CATEGORIES_URL = API_URL + '/categories'
PRODUCTS_URL = API_URL + '/products'
IMAGES_URL = API_URL + '/images'
PRODUCTS_IMAGES_URL = IMAGES_URL + '/products'
STOCK_AVAILABLES_URL = API_URL + '/stock_availables'

# Scraping results file location (now points directly to scraper output)
SCRAPING_RESULST_DIRECTORY = os.path.join(os.path.dirname(__file__), "..","winohobby_data")
SCRAPING_CATEGORIES_FILE = os.path.join(SCRAPING_RESULST_DIRECTORY, "categories.json")
SCRAPING_PRODUCTS_FILE = os.path.join(SCRAPING_RESULST_DIRECTORY, "products.json")

# Other
POST_HEADERS = {'Content-Type': 'application/xml; charset=UTF-8'}

CATEGORIES_IDS_OUTPUT_FILE = "categories_ids.json"
LOG_FILE = 'app.log'
LOGGING_ENABLED = True
    
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s', filemode='a')    

def log_message(message):
    if LOGGING_ENABLED:
        logging.info(message)
