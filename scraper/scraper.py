from bs4 import BeautifulSoup
import requests
import os
import csv
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor

class WebScraper:
    def __init__(self):
        self.base_url = "https://winohobby.biz/"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
        self.output_folder = "winohobby_data"
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(os.path.join(self.output_folder, "images"), exist_ok=True)
        self.products_dictionary = {}
        self.category_name_to_id = {}


    def get_page(self, url):
        try:
            response = self.session.get(url, timeout=10)
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

    # def scrape_categories(self, url=None, parent_name="", visited_urls=None):
    #     if visited_urls is None:
    #         visited_urls = set()
            
    #     if url is None:
    #         url = self.base_url
            
    #     if url in visited_urls:
    #         return []
    #     visited_urls.add(url)
            
    #     html = self.get_page(url)
    #     if not html:
    #         return []
        
    #     soup = BeautifulSoup(html, 'html.parser')
    #     categories = []
        
    #     # Looking for main categories on the homepage
    #     if parent_name == "":
    #         menu_container = soup.select_one("div.innerbox ul.standard")
    #         if not menu_container:
    #             print("Category container not found.")
    #             return []
            
    #         for li in menu_container.find_all("li", recursive=False):
    #             a = li.find("a", recursive=False)
    #             if not a:
    #                 continue
                
    #             name = a.get_text(strip=True)
    #             name = name.replace('<', '-').replace('>', '-')
    #             href = a.get("href")
    #             full_url = urljoin(self.base_url, href)
                
    #             if self.page_has_products_or_subcats(full_url):
    #                 categories.append((name, full_url))
    #                 print(f"Found category: {name}")
    #             else:
    #                 print(f"Skipped empty category: {name} - {full_url}")
                
    #             # Check for subcategories
    #             if len(parent_name.split(' > ')) < 2:
    #                 subcategories = self.scrape_categories(full_url, name, visited_urls)
    #                 categories.extend(subcategories)
        
    #     # On category pages, look for subcategories
    #     else:
    #         depth = len(parent_name.split(' > '))
    #         if depth >= 3:
    #             return categories
            
    #         leftcol = soup.select_one("div.leftcol")

    #         if leftcol:
    #             current_category_item = None
                
    #             category_items = leftcol.select("li")
    #             for li_item in category_items:
    #                 # Check if this is the current category element
    #                 main_link = li_item.find("a", recursive=False)
    #                 if main_link:
    #                     main_href = main_link.get("href", "")
    #                     # Check if the link leads to the current category
    #                     if main_href and (url.endswith(main_href) or main_href in url):
    #                         current_category_item = li_item
    #                         break
                
    #             if current_category_item:
    #                 subcategory_list = current_category_item.find("ul", recursive=False)
    #                 if subcategory_list:
    #                     subcategory_links = subcategory_list.find_all("a", recursive=True)
                        
    #                     for link in subcategory_links:
    #                         href = link.get("href")
    #                         name = link.get_text(strip=True)
    #                         name = name.replace('<', '-').replace('>', '-')
                            
    #                         if not href or not name:
    #                             continue
                            
    #                         # Check if this is a category link
    #                         if not '/c/' in href:
    #                             continue
                                
    #                         full_url = urljoin(self.base_url, href)
                            
    #                         if full_url in visited_urls:
    #                             continue
                            
    #                         main_categories = [
    #                             '/c/Promocje-i-Wyprzedaze/', '/c/DROZDZE-TURBO-HURT/', '/c/FACHOWA-LITERATURA/',
    #                             '/c/Wodki%2C-nalewki%2C-destylacja/', '/c/Akcesoria-PIWOWARSKIE/', '/c/Akcesoria-SEROWARSKIE/', 
    #                             '/c/Akcesoria-WINIARSKIE/', '/c/Akcesoria-Wedliniarskie-Kuchenne/', '/c/Akcesoria-laboratoryjne%2C-dodatki%2C-gadzety/',
    #                             '/c/Butelki%2C-sloje%2C-kapturki%2C-dodatki/', '/c/Platki-debowe/', '/c/WYPRZEDAZE/'
    #                         ]
                            
    #                         is_main_category = any(main_cat.rstrip('/') in href for main_cat in main_categories)
                            
    #                         if not is_main_category:
    #                             full_name = f"{parent_name} > {name}"
    #                             if self.page_has_products_or_subcats(full_url):
    #                                 categories.append((full_name, full_url))
    #                                 print(f"Found subcategory: {full_name}")
    #                             else:
    #                                 print(f"Skipped empty subcategory: {full_name} - {full_url}")
                                
    #                             # Check for further subcategories
    #                             if depth < 2:
    #                                 sub_subcategories = self.scrape_categories(full_url, full_name, visited_urls)
    #                                 categories.extend(sub_subcategories)
            
    #         # Check centercol for other subcategories
    #         centercol = soup.select_one("div.centercol")
    #         if centercol:
    #             error_box = centercol.select("#box_404")
    #             if error_box:
    #                 print(f"Category page shows 404 error: {url}")
    #                 return categories
                
    #             # Search for category links in the main content
    #             category_links = centercol.select("a[href*='/c/']")
                
    #             current_url_parts = url.rstrip('/').split('/')
    #             current_base = '/'.join(current_url_parts)
                
    #             for link in category_links:
    #                 href = link.get("href")
    #                 name = link.get_text(strip=True)
    #                 name = name.replace('<', '-').replace('>', '-')
                    
    #                 if not href or not name:
    #                     continue
                    
    #                 # Skip special and non-category links
    #                 if (name in ['»', '«', '...', '', 'zobacz więcej'] or 
    #                     name.isdigit() or 
    #                     '/full' in href):
    #                     continue
                    
    #                 # Skip links to the same category or its pages
    #                 if (href == url or 
    #                     current_base in href):
    #                     continue
                    
    #                 full_url = urljoin(self.base_url, href)
                    
    #                 if full_url in visited_urls:
    #                     continue
                    
    #                 # Check if this is not a main category from our list
    #                 main_categories = [
    #                     '/c/Promocje-i-Wyprzedaze/', '/c/DROZDZE-TURBO-HURT/', '/c/FACHOWA-LITERATURA/',
    #                     '/c/Wodki%2C-nalewki%2C-destylacja/', '/c/Akcesoria-PIWOWARSKIE/', '/c/Akcesoria-SEROWARSKIE/', 
    #                     '/c/Akcesoria-WINIARSKIE/', '/c/Akcesoria-Wedliniarskie-Kuchenne/', '/c/Akcesoria-laboratoryjne%2C-dodatki%2C-gadzety/',
    #                     '/c/Butelki%2C-sloje%2C-kapturki%2C-dodatki/', '/c/Platki-debowe/', '/c/WYPRZEDAZE/'
    #                 ]
                    
    #                 is_main_category = any(main_cat.rstrip('/') in href for main_cat in main_categories)
                    
    #                 # Dodaj tylko te które nie są głównymi kategoriami
    #                 if not is_main_category:
    #                     # Sprawdź czy już nie mamy tej kategorii (żeby uniknąć duplikatów)
    #                     full_name = f"{parent_name} > {name}"
    #                     if not any(cat_name == full_name for cat_name, _ in categories):
    #                         if self.page_has_products_or_subcats(full_url):
    #                             categories.append((full_name, full_url))
    #                             print(f"Found subcategory: {full_name}")
    #                         else:
    #                             print(f"Skipped empty subcategory: {full_name} - {full_url}")
                            
    #                         # Sprawdź dalsze podkategorie tylko jeśli nie za głęboko
    #                         if depth < 2:
    #                             sub_subcategories = self.scrape_categories(full_url, full_name, visited_urls)
    #                             categories.extend(sub_subcategories)
        
    #     return categories

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
        
        # Looking for main categories on the homepage
        if parent_name == "":
            menu_container = soup.select_one("div.innerbox ul.standard")
            if not menu_container:
                print("Category container not found.")
                return []
            
            for li in menu_container.find_all("li", recursive=False):
                a = li.find("a", recursive=False)
                if not a:
                    continue
                
                name = a.get_text(strip=True)
                name = name.replace('<', '-').replace('>', '-')
                href = a.get("href")
                full_url = urljoin(self.base_url, href)
                
                # Add the category even if it is empty
                categories.append((name, full_url))
                if self.page_has_products_or_subcats(full_url):
                    print(f"Found category: {name}")
                else:
                    print(f"Added empty category: {name} - {full_url}")
                
                # Check for subcategories
                if len(parent_name.split(' > ')) < 2:
                    subcategories = self.scrape_categories(full_url, name, visited_urls)
                    categories.extend(subcategories)
        
        # On category pages, look for subcategories
        else:
            depth = len(parent_name.split(' > '))
            if depth >= 3:
                return categories
            
            leftcol = soup.select_one("div.leftcol")

            if leftcol:
                current_category_item = None
                
                category_items = leftcol.select("li")
                for li_item in category_items:
                    # Check if this is the current category element
                    main_link = li_item.find("a", recursive=False)
                    if main_link:
                        main_href = main_link.get("href", "")
                        # Check if the link leads to the current category
                        if main_href and (url.endswith(main_href) or main_href in url):
                            current_category_item = li_item
                            break
                
                if current_category_item:
                    subcategory_list = current_category_item.find("ul", recursive=False)
                    if subcategory_list:
                        subcategory_links = subcategory_list.find_all("a", recursive=True)
                        
                        for link in subcategory_links:
                            href = link.get("href")
                            name = link.get_text(strip=True)
                            name = name.replace('<', '-').replace('>', '-')
                            
                            if not href or not name:
                                continue
                            
                            # Check if this is a category link
                            if not '/c/' in href:
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
                            
                            # Check for further subcategories
                            if depth < 2:
                                sub_subcategories = self.scrape_categories(full_url, full_name, visited_urls)
                                categories.extend(sub_subcategories)
        
        return categories

    def scrape_products_from_category(self, category_url, category_name):
        print("Scraping products from category:", category_name)
        html = self.get_page(category_url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        
        product_links = set()
        for a in soup.select("a.product-name, .product-item a, .product a, .product-link"):
            href = a.get("href")
            if href and "/pl/p/" in href:
                product_links.add(urljoin(self.base_url, href))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.scrape_product, url, category_name) for url in product_links]
            for future in futures:
                future.result()

        # pagination
        pagination = soup.select("div.floatcenterwrap ul.paginator li a")
        next_page_url = None
        for a in pagination:
            if a.get_text(strip=True) == "»":  # next page arrow
                next_page_url = urljoin(self.base_url, a["href"])
                break
        if next_page_url:
            self.scrape_products_from_category(next_page_url, category_name)

    def scrape_product(self, product_url, category_name):

        if product_url in self.products_dictionary:
            self.products_dictionary[product_url]["categories"].add(category_name)
            return

        print("Scraping product:", product_url)
        html = self.get_page(product_url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        
        name = soup.select_one("h1[itemprop='name']")
        name = name.text.strip() if name else "N/A"
        name = name.replace('<', '-').replace('>', '-').replace('=', '-')

        friendly_url = name.lower().replace('?','').replace('°','').replace('½','pol').replace('&', '-').replace('„', '').replace('”','').replace('*','').replace('%', '').replace('’', '-').replace('–','-').replace(',', '-').replace('.','-').replace(':', '-').replace('\'', '-').replace('\"','-').replace('+', '-').replace(' ', '-').replace('/', '-').replace(',', '').replace('(', '').replace(')', '').replace('ł', 'l').replace('ą', 'a').replace('ę', 'e').replace('ś', 's').replace('ć', 'c').replace('ń', 'n').replace('ó', 'o').replace('ź', 'z').replace('ż', 'z').replace('<', '-').replace('>', '-')
        friendly_url = '-'.join(filter(None, friendly_url.split('-'))) # Removes extra dashes

        price_tag = soup.select_one("em.main-price, span.main-price, span.price")
        if price_tag:
            price = price_tag.get_text(strip=True)
        else:
            price = "N/A"

        desc = soup.select_one("div[itemprop='description'].resetcss.fr-view")
        if desc:
            description = " ".join(p.get_text(strip=True) for p in desc.find_all(['p', 'li', 'h2', 'h3']) if p.get_text(strip=True))
        else:
            description = "N/A"
        
        images = []
        for img_tag in soup.select("a[href^='/userdata/public/gfx/'], img[src^='/userdata/public/gfx/']"):
            img_url = img_tag.get("href") or img_tag.get("src")
            if img_url and len(images) < 2:
                img_full = urljoin(self.base_url, img_url)
                images.append(img_full)
        
        downloaded_images = []
        for img_url in images:
            filename = os.path.join(self.output_folder, "images", os.path.basename(img_url))
            self.download_image(img_url, filename)
            downloaded_images.append(filename)

        product_data = {
            "name": name,
            "price": price,
            "description": description,
            "images": images,
            "categories": set([category_name]),
            "url": friendly_url
        }
        
        self.products_dictionary[product_url] = product_data
        time.sleep(0.5)

    def download_image(self, img_url, filename):
        try:
            response = self.session.get(img_url, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except:
            print("Failed to download image:", img_url)
    
    def save_to_csv(self):
        """
        Zapisuje kategorie do pliku CSV w formacie kompatybilnym z PrestaShop.
        
        Pola PrestaShop:
        - Aktywny: 1 (aktywna)
        - Nazwa: nazwa kategorii
        - Kategoria
        - Cena
        - Opis
        - Dostępne do zamówienia: 1
        - W sprzedaży: 1
        - Ilość: 100
        - Meta-tytuł: tytuł SEO
        - Przepisany URL: przyjazny URL
        - URL zdjęć
        """
        csv_path = os.path.join(self.output_folder, "products.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            
            writer.writerow([
                "Aktywny", "Nazwa", "Cena", "Opis", "Dostępne do zamówienia", "W sprzedaży", "Ilość","URL zdjęć", "Kategorie", "Przepisany URL"
            ])

            for product in self.products_dictionary.values():
                name = product["name"]
                price = product["price"].replace(' zł', '').replace(',', '.') if product["price"] else "0"
                description = product["description"]
                
                # Keep only the deepest (leaf) categories for this product.
                # product["categories"] contains category paths like 'A > B > C' or main 'A'.
                raw_cats = [c.strip() for c in product.get("categories", []) if c and c.strip()]

                # Remove any category that is a parent of another category in the set.
                deepest = []
                for c in raw_cats:
                    is_parent = any((other != c and other.startswith(c + ' > ')) for other in raw_cats)
                    if not is_parent:
                        deepest.append(c)

                # Map deepest category paths to IDs using the mapping created in save_categories_csv.
                # If exact path not found, fall back to matching by leaf name.
                category_ids = []
                for cat_path in deepest:
                    cat_id = self.category_name_to_id.get(cat_path)
                    if not cat_id:
                        leaf = cat_path.split(' > ')[-1]
                        # try to find any category whose leaf matches
                        for key, val in self.category_name_to_id.items():
                            if key.split(' > ')[-1] == leaf:
                                cat_id = val
                                break
                    # If still not found, keep the original name as fallback
                    category_ids.append(cat_id if cat_id else cat_path)

                categories = "|".join(category_ids)
                image_urls = "|".join(product["images"])
                
                writer.writerow([
                    "1",
                    name,
                    price,
                    description,
                    "1",
                    "1",
                    "100",
                    image_urls,
                    categories,
                    product["url"]
                ])

        print(f"Number of products: {len(self.products_dictionary)}")     

    def save_categories_csv(self, categories):
        """
        Zapisuje kategorie do pliku CSV w formacie kompatybilnym z PrestaShop.
        
        Pola PrestaShop:
        - ID: pozostaw puste, PrestaShop automatycznie przypisze
        - Aktywny: 1 (aktywna)
        - Nazwa: nazwa kategorii
        - Kategoria nadrzędna: nazwa kategorii nadrzędnej lub puste dla głównych
        - Główna kategoria: 1 dla głównych kategorii, 0 dla podkategorii
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
                "Główna kategoria (0/1)",
                "Meta-tytuł",
                "Opis meta",
                "Przepisany URL"
            ])
            
            category_id = 10 # Start from 10 to avoid conflicts with default categories
            for cat_name in unique_categories:
                if cat_name not in category_map:
                    continue
                    
                cat_info = category_map[cat_name]
                parts = cat_info['parts']
                
                category_name = parts[-1]

                self.category_name_to_id[cat_name] = str(category_id)
                
                parent_category = ""
                if len(parts) > 1:
                    parent_category = parts[-2]
                
                is_main_category = 1 if len(parts) == 1 else 0
                
                friendly_url = category_name.lower().replace('\'', '-').replace('\"','-').replace('+', '-').replace('&', 'and').replace(' ', '-').replace('/', '-').replace(',', '').replace('(', '').replace(')', '').replace('ł', 'l').replace('ą', 'a').replace('ę', 'e').replace('ś', 's').replace('ć', 'c').replace('ń', 'n').replace('ó', 'o').replace('ź', 'z').replace('ż', 'z')
                
                meta_title = f"{category_name} - WinoHobby"
                
                meta_description = f"Akcesoria i produkty z kategorii {category_name}. Wysokiej jakości artykuły w najlepszych cenach."
                
                writer.writerow([
                    str(category_id),
                    "1",
                    category_name,
                    parent_category,
                    str(is_main_category),
                    meta_title,
                    meta_description,
                    friendly_url
                ])
                category_id += 1

    def scrape(self):
        start_time = time.time()
        print("Started Scraping")
        categories = self.scrape_categories()

        # Normalize and deduplicate categories to avoid processing the same
        # category multiple times (differences can be only trailing slash/case).
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

        self.save_to_csv()
        end_time = time.time()
        print(f"\nScraping took {end_time - start_time:.2f} seconds")
        print("Scraping completed. Data saved to", self.output_folder)

def main():
    scraper = WebScraper()
    scraper.scrape()
if __name__ == "__main__":
    main()