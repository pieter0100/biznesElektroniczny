import os
import csv
import time
import random
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

class WebScraper:
    BASE_URL = "https://winohobby.biz/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    OUTPUT_FOLDER = "winohobby_data"
    IMAGE_FOLDER = os.path.join(OUTPUT_FOLDER, "images")
    START_CATEGORY_ID = 3
    MAX_IMAGES_PER_PRODUCT = 2
    THREAD_POOL_SIZE = 10
    TIMEOUT = 10  # seconds

    def __init__(self):
        self.base_url = self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT
            })
        self.output_folder = self.OUTPUT_FOLDER
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.IMAGE_FOLDER, exist_ok=True)
        self.products_dictionary = {}
        self.category_name_to_id = {}


    def get_page(self, url):
        try:
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"Error while downloading {url}: {e}")
            return None

    def page_has_products_or_subcats(self, url):
        """Return True if the category page contains product links or subcategory links.
        This helps skip empty categories that have no products or further subcategories.
        """
        html = self.get_page(url)
        if not html:
            return False
        soup = BeautifulSoup(html, 'html.parser')
        # product links
        if soup.select("a[href*='/pl/p/']"):
            return True
        # subcategory links (category pages)
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
        """Scrape main categories from the homepage."""
        categories = []
        menu_container = soup.select_one("div.innerbox ul.standard")
        if not menu_container:
            print("Category container not found.")
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
                print(f"Found category: {name}")
            else:
                print(f"Added empty category: {name} - {full_url}")

            # Recursively scrape subcategories
            subcategories = self.scrape_categories(full_url, name, visited_urls)
            categories.extend(subcategories)

        return categories
    
    def scrape_subcategories(self, soup, url, parent_name, visited_urls):
        """Scrape subcategories from a category page."""
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
        """Find the current category item in the left column."""
        for li_item in leftcol.select("li"):
            main_link = li_item.find("a", recursive=False)
            if main_link:
                main_href = main_link.get("href", "")
                if main_href and (url.endswith(main_href) or main_href in url):
                    return li_item
        return None
    
    def extract_subcategories(self, subcategory_list, parent_name, visited_urls):
        """Extract subcategories from a subcategory list."""
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
                print(f"Found subcategory: {full_name}")
            else:
                print(f"Added empty subcategory: {full_name} - {full_url}")

            # Recursively scrape further subcategories
            categories.extend(self.scrape_categories(full_url, full_name, visited_urls))

        return categories

    def scrape_products_from_category(self, category_url, category_name):
        print("Scraping products from category:", category_name)
        html = self.get_page(category_url)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        product_links = self.get_product_links(soup)

        self.scrape_products_concurrently(product_links, category_name)
        self.handle_pagination(soup, category_url, category_name)

    def get_product_links(self, soup):
        """Extract product links from a category page."""
        product_links = set()
        for a in soup.select("a.product-name, .product-item a, .product a, .product-link"):
            href = a.get("href")
            if href and "/pl/p/" in href:
                product_links.add(urljoin(self.base_url, href))
        return product_links

    def scrape_products_concurrently(self, product_links, category_name):
        """Scrape product details concurrently using a thread pool."""
        with ThreadPoolExecutor(max_workers=self.THREAD_POOL_SIZE) as executor:
            futures = [executor.submit(self.scrape_product, url, category_name) for url in product_links]
            for future in futures:
                future.result()

    def handle_pagination(self, soup, category_url, category_name):
        """Handle pagination for a category page."""
        pagination = soup.select("div.floatcenterwrap ul.paginator li a")
        next_page_url = None
        for a in pagination:
            if a.get_text(strip=True) == "»":  # next page arrow
                next_page_url = urljoin(self.base_url, a["href"])
                break
        if next_page_url:
            self.scrape_products_from_category(next_page_url, category_name)

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

    def scrape_product(self, product_url, category_name):
        if product_url in self.products_dictionary:
            self.products_dictionary[product_url]["categories"].add(category_name)
            return

        print("Scraping product:", product_url)
        html = self.get_page(product_url)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        product_data = self.extract_product_details(soup, category_name)
        self.products_dictionary[product_url] = product_data
        time.sleep(0.5)

    def extract_product_details(self, soup, category_name):
        """Extract product details from the product page."""
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
            filename = os.path.join(self.output_folder, "images", os.path.basename(img_url))
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
        """Extract the product manufacturer (Producent) from possible HTML patterns.
        """
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
        """Extract the product code."""
        span = soup.select_one("div.row.code span")
        if span:
            code = span.get_text(strip=True)
            if code and code != "-":
                return code
        return "-"

    def get_product_name(self, soup):
        """Extract the product name."""
        name = soup.select_one("h1[itemprop='name']")
        return name.text.strip() if name else "N/A"

    def get_product_price(self, soup):
        """Extract the product price."""
        price_tag = soup.select_one("em.main-price, span.main-price, span.price")
        if not price_tag:
            return "N/A"
        raw = price_tag.get_text(strip=True) 
        norm = raw.replace('\xa0', ' ').replace(' ', '').replace(',', '.').replace('zł', '')
        return norm

    def get_product_description(self, soup):
        """Extract the product description."""
        desc = soup.select_one("div[itemprop='description'].resetcss.fr-view")
        if desc:
            return " ".join(p.get_text(strip=True) for p in desc.find_all(['p', 'li', 'h2', 'h3']) if p.get_text(strip=True))
        return "N/A"

    def get_product_images(self, soup):
        """Extract product image URLs."""
        images = []
        for img_tag in soup.select("a[href^='/userdata/public/gfx/'], img[src^='/userdata/public/gfx/']"):
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
        except:
            print("Failed to download image:", img_url)
    
    def get_parent_category_id(self, parts):
        if len(parts) == 1:
            return "2"

        parent_full = ' > '.join(parts[:-1])
        parent_category = self.category_name_to_id.get(parent_full, "")

        # fallback: match parent by last segment
        if not parent_category:
            parent_leaf = parts[-2]
            for key, val in self.category_name_to_id.items():
                if key.split(' > ')[-1] == parent_leaf:
                    return val

        return parent_category

    def get_deepest_category_ids(self, product_categories):
        """
        Given a list of raw category paths for a product, returns a list of
        mapped PrestaShop category IDs that are the deepest in the hierarchy.
        """
        raw_cats = [c.strip() for c in product_categories if c and c.strip()]

        deepest = []
        for c in raw_cats:
            is_parent = any(
                (other != c and other.startswith(c + ' > '))
                for other in raw_cats
            )
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
        """
        Saves products to a CSV file in a format compatible with PrestaShop.
        
        PrestaShop fields:
        - Indeks #: product code
        - Aktywny (0 lub 1): 1 (active)
        - Nazwa: product name
        - ID reguły podatku: 1
        - Cena bez podatku. (netto): price without tax
        - Cena zawiera podatek. (brutto): price with tax
        - Marka: manufacturer
        - Opis: product description
        - Dostępne do zamówienia (0 = Nie, 1 = Tak): 1
        - W sprzedaży (0 lub 1): 1
        - Ilość: random number between 0 and 10
        - Meta-tytuł: SEO title
        - Kategorie (x,y,z...): category IDs separated by |
        - Adresy URL zdjęcia (x,y,z...): image URLs separated by |
        - Przepisany URL: friendly URL
        """
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
                "W sprzedaży (0 lub 1)", 
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
                price_netto = str(round(float(price_brutto) / 1.23, 2)) if price_brutto != "0" else "0" #
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
                    "1",
                    random.randint(0,10),
                    image_urls,
                    categories,
                    product["url"]
                ])

        print(f"Number of products: {len(self.products_dictionary)}")     

    def save_categories_csv(self, categories):
        """
        Saves categories to a CSV file in a format compatible with PrestaShop.
        
        PrestaShop fields:
        - ID: pozostaw puste, PrestaShop automatycznie przypisze
        - Aktywny: 1 (aktywna)
        - Nazwa: nazwa kategorii
        - Kategoria nadrzędna: nazwa kategorii nadrzędnej lub puste dla głównych
        - Opis: opis kategorii (może być pusty)
        - Meta-tytuł: tytuł SEO (może być pusty)
        - Opis meta: opis SEO (może być pusty)
        - Przepisany URL: przyjazny URL (może być pusty)
        - URL zdjęcia: URL do zdjęcia kategorii (może być pusty)
        """
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

    def scrape(self):
        start_time = time.time()
        print("Started Scraping")
        categories = self.scrape_categories()

        # Deduplicate categories to avoid processing the same
        # category multiple times.
        seen = set()
        deduped_categories = []
        for name, url in categories:
            name_norm = " ".join(name.split()).strip()
            url_norm = url.rstrip('/') if isinstance(url, str) else url
            key = (name_norm.lower(), url_norm.lower() if isinstance(url_norm, str) else url_norm)
            if key in seen:
                continue
            seen.add(key)
            deduped_categories.append((name_norm, url_norm))

        categories = deduped_categories

        self.save_categories_csv(categories)
        for category_name, category_url in categories:
            print("Category:", category_name)
            self.scrape_products_from_category(category_url, category_name)

        self.save_products_to_csv()
        end_time = time.time()
        print(f"\nScraping took {end_time - start_time:.2f} seconds")
        print("Scraping completed. Data saved to", self.output_folder)

def main():
    scraper = WebScraper()
    scraper.scrape()

if __name__ == "__main__":
    main()