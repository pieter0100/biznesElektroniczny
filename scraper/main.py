from categories_scraper import CategoriesScraper
from products_scraper import ProductsScraper
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Console handler (INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))

# Rotating file handler (DEBUG)
fh = RotatingFileHandler('scraper.log', maxBytes=2_000_000, backupCount=3, encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))

if not logger.handlers:
    logger.addHandler(ch)
    logger.addHandler(fh)

# Quiet down noisy libs
logging.getLogger('requests').setLevel(logging.WARNING)


def main():
    logging.info('Starting scraping run')
    # 1) Scrape categories and save CSV; get category mapping
    cat_scraper = CategoriesScraper()
    categories, category_map = cat_scraper.run()

    # 2) Scrape products using category mapping and save CSV
    prod_scraper = ProductsScraper(category_map)
    prod_scraper.run(categories)
    logging.info('Scraping run finished')


if __name__ == "__main__":
    main()
