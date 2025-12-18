import os
import csv
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)

class CategoriesScraper:
    BASE_URL = "https://winohobby.biz/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "..","winohobby_data")
    START_CATEGORY_ID = 3

    def __init__(self):
        self.base_url = self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT
        })
        self.output_folder = self.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
        self.category_name_to_id = {}

    def get_page(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error while downloading {url}: {e}")
            return None

    def page_has_products_or_subcats(self, url):
        html = self.get_page(url)
        if not html:
            return False
        soup = BeautifulSoup(html, 'html.parser')
        if soup.select("a[href*='/pl/p/']"):
            return True
        if soup.select("a[href*='/c/']"):
            return True
        return False

    def clean_name(self, name):
        return name.replace('<', '-').replace('>', '-').replace('=', '-').replace('.', '-')

    def scrape_categories(self, url=None, parent_name="", visited_urls=None):
        if visited_urls is None:
            visited_urls = set()
        if url is None:
            url = self.base_url
        if url in visited_urls:
            return []
        visited_urls.add(url)

        html = self.get_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        categories = []

        if parent_name == "":
            categories.extend(self.scrape_main_categories(soup, visited_urls))
        else:
            categories.extend(self.scrape_subcategories(soup, url, parent_name, visited_urls))

        return categories

    def scrape_main_categories(self, soup, visited_urls):
        categories = []
        menu_container = soup.select_one("div.innerbox ul.standard")
        if not menu_container:
            logger.warning("Category container not found.")
            return []

        for li in menu_container.find_all("li", recursive=False):
            a = li.find("a", recursive=False)
            if not a:
                continue

            name = self.clean_name(a.get_text(strip=True))
            href = a.get("href")
            full_url = urljoin(self.base_url, href)

            categories.append((name, full_url))
            if self.page_has_products_or_subcats(full_url):
                logger.info(f"Found category: {name}")
            else:
                logger.info(f"Added empty category: {name} - {full_url}")

            subcategories = self.scrape_categories(full_url, name, visited_urls)
            categories.extend(subcategories)

        return categories

    def scrape_subcategories(self, soup, url, parent_name, visited_urls):
        categories = []
        depth = len(parent_name.split(' > '))
        if depth >= 3:
            return categories

        leftcol = soup.select_one("div.leftcol")
        if not leftcol:
            return categories

        current_category_item = self.find_current_category_item(leftcol, url)
        if current_category_item:
            subcategory_list = current_category_item.find("ul", recursive=False)
            if subcategory_list:
                categories.extend(self.extract_subcategories(subcategory_list, parent_name, visited_urls))

        return categories

    def find_current_category_item(self, leftcol, url):
        for li_item in leftcol.select("li"):
            main_link = li_item.find("a", recursive=False)
            if main_link:
                main_href = main_link.get("href", "")
                if main_href and (url.endswith(main_href) or main_href in url):
                    return li_item
        return None

    def extract_subcategories(self, subcategory_list, parent_name, visited_urls):
        categories = []
        for link in subcategory_list.find_all("a", recursive=True):
            href = link.get("href")
            name = self.clean_name(link.get_text(strip=True))
            if not href or not name or '/c/' not in href:
                continue

            full_url = urljoin(self.base_url, href)
            if full_url in visited_urls:
                continue

            full_name = f"{parent_name} > {name}"
            categories.append((full_name, full_url))
            if self.page_has_products_or_subcats(full_url):
                logger.info(f"Found subcategory: {full_name}")
            else:
                logger.info(f"Added empty subcategory: {full_name} - {full_url}")

            categories.extend(self.scrape_categories(full_url, full_name, visited_urls))

        return categories

    def name_to_friendly_url(self, name):
        replacement = {
        '?': '', '°': '', '½': 'pol', '&': '-', '„': '', '”': '', '\"': '-','<': '-',
        '*': '', '%': '', '’': '-', '–': '-', ',': '-', '.': '-', '\'': '-', '>': '-',
        ':': '-', "'": '-', '"': '-', '+':'-', ' ':'-', '/':'-', '(':'', ')':'', '=':'-',
        'ł':'l','ą':'a','ę':'e','ś':'s','ć':'c','ń':'n','ó':'o','ź':'z','ż':'z',
        'Ł':'L','Ą':'A','Ę':'E','Ś':'S','Ć':'C','Ń':'N','Ó':'O','Ź':'Z','Ż':'Z'
        }
        for key, value in replacement.items():
            name = name.replace(key, value)
        return "-".join(filter(None, name.lower().split("-")))

    def get_parent_category_id(self, parts):
        if len(parts) == 1:
            return "2"
        parent_full = ' > '.join(parts[:-1])
        parent_category = self.category_name_to_id.get(parent_full, "")
        if not parent_category:
            parent_leaf = parts[-2]
            for key, val in self.category_name_to_id.items():
                if key.split(' > ')[-1] == parent_leaf:
                    return val
        return parent_category

    def save_categories_csv(self, categories):
        csv_path = os.path.join(self.output_folder, "categories.csv")
        category_map = {}
        category_hierarchy = {}

        for name, url in categories:
            parts = name.split(' > ')
            category_map[name] = {
                'url': url,
                'parts': parts,
                'level': len(parts)
            }
            if len(parts) > 1:
                parent_name = ' > '.join(parts[:-1])
                category_hierarchy[name] = parent_name
            else:
                category_hierarchy[name] = None

        unique_categories = []
        processed = set()

        def add_category_and_parents(cat_name):
            if cat_name in processed:
                return
            if cat_name in category_hierarchy and category_hierarchy[cat_name]:
                add_category_and_parents(category_hierarchy[cat_name])
            if cat_name not in processed:
                unique_categories.append(cat_name)
                processed.add(cat_name)

        for name, _ in categories:
            add_category_and_parents(name)

        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([
                "ID",
                "Aktywny (0/1)",
                "Nazwa*",
                "Kategoria nadrzędna",
                "Meta-tytuł",
                "Opis meta",
                "Przepisany URL"
            ])

            category_id = self.START_CATEGORY_ID
            for cat_name in unique_categories:
                if cat_name not in category_map:
                    continue
                cat_info = category_map[cat_name]
                parts = cat_info['parts']
                category_name = parts[-1]
                self.category_name_to_id[cat_name] = str(category_id)
                parent_category = self.get_parent_category_id(parts)
                friendly_url = self.name_to_friendly_url(category_name)
                meta_title = f"{category_name} - WinoHobby"
                meta_description = f"Akcesoria i produkty z kategorii {category_name}. Wysokiej jakości artykuły w najlepszych cenach."
                writer.writerow([
                    str(category_id),
                    "1",
                    category_name,
                    parent_category,
                    meta_title,
                    meta_description,
                    friendly_url
                ])
                category_id += 1

        return self.category_name_to_id

    def run(self):
        start = time.time()
        logger.info("Started Category Scraping")
        categories = self.scrape_categories()
        # Deduplicate
        seen = set()
        deduped = []
        for name, url in categories:
            name_norm = " ".join(name.split()).strip()
            url_norm = url.rstrip('/') if isinstance(url, str) else url
            key = (name_norm.lower(), url_norm.lower() if isinstance(url_norm, str) else url_norm)
            if key in seen:
                continue
            seen.add(key)
            deduped.append((name_norm, url_norm))
        mapping = self.save_categories_csv(deduped)
        end = time.time()
        logger.info(f"Category scraping took {end - start:.2f} seconds")
        return deduped, mapping
