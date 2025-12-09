import os
import csv
import time
import random
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import re

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class ProductsScraper:
    BASE_URL = "https://winohobby.biz/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "winohobby_data")
    IMAGE_FOLDER = os.path.join(OUTPUT_FOLDER, "images")
    MAX_IMAGES_PER_PRODUCT = 2
    THREAD_POOL_SIZE = 10
    TIMEOUT = 10
    TAX = 1.23

    def __init__(self, category_name_to_id):
        self.base_url = self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT
        })
        self.output_folder = self.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.IMAGE_FOLDER, exist_ok=True)
        self.products_dictionary = {}
        self.category_name_to_id = category_name_to_id or {}

    def get_page(self, url):
        try:
            response = self.session.get(url, timeout=self.TIMEOUT)
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

    def scrape_products_from_category(self, category_url, category_name):
        logger.info(f"Scraping products from category: {category_name}")
        html = self.get_page(category_url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        product_links = self.get_product_links(soup)
        self.scrape_products_concurrently(product_links, category_name)
        self.handle_pagination(soup, category_url, category_name)

    def get_product_links(self, soup):
        product_links = set()
        for a in soup.select("a.product-name, .product-item a, .product a, .product-link"):
            href = a.get("href")
            if href and "/pl/p/" in href:
                product_links.add(urljoin(self.base_url, href))
        return product_links

    def scrape_products_concurrently(self, product_links, category_name):
        with ThreadPoolExecutor(max_workers=self.THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(self.scrape_product, url, category_name) for url in product_links]
            for future in futures:
                future.result()

    def handle_pagination(self, soup, category_url, category_name):
        pagination = soup.select("div.floatcenterwrap ul.paginator li a")
        next_page_url = None
        for a in pagination:
            if a.get_text(strip=True) == "»":
                next_page_url = urljoin(self.base_url, a["href"])
                break
        if next_page_url:
            self.scrape_products_from_category(next_page_url, category_name)

    def name_to_friendly_url(self, name):
        replacement = {
            '?': '', '°': '', '½': 'pol', '&': '-', '„': '', '”': '', '"': '-', '<': '-',
            '*': '', '%': '', '’': '-', '–': '-', ',': '-', '.': '-', "'": '-', '>': '-',
            ':': '-', '"': '-', '+': '-', ' ': '-', '/': '-', '(': '', ')': '', '=': '-',
            'ł': 'l', 'ą': 'a', 'ę': 'e', 'ś': 's', 'ć': 'c', 'ń': 'n', 'ó': 'o', 'ź': 'z', 'ż': 'z',
            'Ł': 'L', 'Ą': 'A', 'Ę': 'E', 'Ś': 'S', 'Ć': 'C', 'Ń': 'N', 'Ó': 'O', 'Ź': 'Z', 'Ż': 'Z'
        }
        for key, value in replacement.items():
            name = name.replace(key, value)
        return "-".join(filter(None, name.lower().split("-")))

    def scrape_product(self, product_url, category_name):
        if product_url in self.products_dictionary:
            self.products_dictionary[product_url]["categories"].add(category_name)
            return
        logger.debug(f"Scraping product: {product_url}")
        html = self.get_page(product_url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        product_data = self.extract_product_details(soup, category_name)
        self.products_dictionary[product_url] = product_data
        time.sleep(0.5)

    def sanitize_filename(self, url_or_name: str) -> str:
        base = url_or_name.split('?', 1)[0]
        name = os.path.basename(base)
        # Replace unsafe characters with '-'
        return re.sub(r'[<>:"/\\|?*]+', '-', name)

    def is_generic_placeholder(self, img_url: str) -> bool:
        return '/environment/cache/images/productGfx___overlay_500_500.jpg?overlay=1' in img_url

    def extract_product_details(self, soup, category_name):
        product_code = self.get_product_code(soup)
        name = self.get_product_name(soup)
        name = self.clean_name(name)
        friendly_url = self.name_to_friendly_url(name)
        price = self.get_product_price(soup)
        description = self.get_product_description(soup)
        manufacturer = self.get_product_manufacturer(soup)
        images = self.get_product_images(soup)

        downloaded_images = []
        for img_url in images:
            safe_name = self.sanitize_filename(img_url)
            # If generic placeholder, prefix with product identifier to avoid overwrites
            if self.is_generic_placeholder(img_url):
                product_id = self.get_product_code(soup)
                if not product_id or product_id == '-':
                    product_id = self.name_to_friendly_url(self.get_product_name(soup))
                safe_name = f"{self.sanitize_filename(product_id)}-{safe_name}"
            filename = os.path.join(self.output_folder, "images", safe_name)
            self.download_image(img_url, filename)
            downloaded_images.append(filename)

        return {
            "code": product_code,
            "name": name,
            "price": price,
            "description": description,
            "manufacturer": manufacturer,
            "images": images,
            "categories": set([category_name]),
            "url": friendly_url
        }

    def get_product_manufacturer(self, soup):
        manu = soup.select_one("div.row.manufacturer")
        if manu:
            inner_anchor = manu.select_one("a.brand")
            if inner_anchor:
                title = inner_anchor.get("title")
                if title:
                    t = title.strip()
                    if t and t != "-":
                        return t
                text = inner_anchor.get_text(strip=True)
                if text and text != "-":
                    return text
                img = inner_anchor.find("img")
                if img and img.get("alt"):
                    alt = img.get("alt").strip()
                    if alt and alt != "-":
                        return alt
            em = manu.find("em")
            if em:
                parts = [s for s in manu.stripped_strings]
                if len(parts) >= 2:
                    candidate = parts[1].strip()
                    if candidate and candidate != "-":
                        return candidate
        return "-"

    def get_product_code(self, soup):
        span = soup.select_one("div.row.code span")
        if span:
            code = span.get_text(strip=True)
            if code and code != "-":
                return code
        return "-"

    def get_product_name(self, soup):
        name = soup.select_one("h1[itemprop='name']")
        return name.text.strip() if name else "N/A"

    def get_product_price(self, soup):
        price_tag = soup.select_one("em.main-price, span.main-price, span.price")
        if not price_tag:
            return "N/A"
        raw = price_tag.get_text(strip=True)
        norm = raw.replace('\xa0', ' ').replace(' ', '').replace(',', '.').replace('zł', '')
        return norm

    def get_product_description(self, soup):
        desc = soup.select_one("div[itemprop='description'].resetcss.fr-view")
        if desc:
            return " ".join(p.get_text(strip=True) for p in desc.find_all(['p', 'li', 'h2', 'h3']) if p.get_text(strip=True))
        return "N/A"

    def get_product_images(self, soup):
        images = []
        for img_tag in soup.select("a[href^='/userdata/public/gfx/'], img[src^='/userdata/public/gfx/'], img[src^='/environment/cache/images/']"):
            img_url = img_tag.get("href") or img_tag.get("src")
            if img_url and len(images) < self.MAX_IMAGES_PER_PRODUCT:
                images.append(urljoin(self.base_url, img_url))
        return images

    def download_image(self, img_url, filename):
        try:
            response = self.session.get(img_url, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            logger.warning(f"Failed to download image: {img_url}. Error: {e}")

    def get_deepest_category_ids(self, product_categories):
        raw_cats = [c.strip() for c in product_categories if c and c.strip()]
        deepest = []
        for c in raw_cats:
            is_parent = any((other != c and other.startswith(c + ' > ')) for other in raw_cats)
            if not is_parent:
                deepest.append(c)
        category_ids = []
        for cat_path in deepest:
            cat_id = self.category_name_to_id.get(cat_path)
            if not cat_id:
                leaf = cat_path.split(' > ')[-1]
                for key, val in self.category_name_to_id.items():
                    if key.split(' > ')[-1] == leaf:
                        cat_id = val
                        break
            category_ids.append(cat_id if cat_id else cat_path)
        return category_ids

    def save_products_to_csv(self):
        csv_path = os.path.join(self.output_folder, "products.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([
                "Indeks #",
                "Aktywny (0 lub 1)",
                "Nazwa",
                "ID reguły podatku",
                "Cena bez podatku. (netto)",
                "Cena zawiera podatek. (brutto)",
                "Marka",
                "Opis",
                "Dostępne do zamówienia (0 = Nie, 1 = Tak)",
                "Ilość",
                "Adresy URL zdjęcia (x,y,z...)",
                "Kategorie (x,y,z...)",
                "Przepisany URL"
            ])
            for product in self.products_dictionary.values():
                product_code = product.get("code", "")
                name = product["name"]
                manufacturer = product.get("manufacturer", "")
                price_brutto = product.get("price") or "0"
                price_netto = str(round(float(price_brutto) / self.TAX, 2)) if price_brutto != "0" else "0"
                description = product["description"]
                category_ids = self.get_deepest_category_ids(product.get("categories", []))
                categories = "|".join(category_ids)
                image_urls = "|".join(product["images"])
                writer.writerow([
                    product_code,
                    "1",
                    name,
                    "1",
                    price_netto,
                    price_brutto,
                    manufacturer,
                    description,
                    "1",
                    random.randint(0, 10),
                    image_urls,
                    categories,
                    product["url"]
                ])
        logger.info(f"Number of products: {len(self.products_dictionary)}")

    def run(self, categories):
        start = time.time()
        for category_name, category_url in categories:
            logger.info(f"Category: {category_name}")
            self.scrape_products_from_category(category_url, category_name)
        self.save_products_to_csv()
        end = time.time()
        logger.info(f"Product scraping took {end - start:.2f} seconds")
