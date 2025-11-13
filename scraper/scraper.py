from bs4 import BeautifulSoup
import requests
import os
import csv
from urllib.parse import urljoin
import time

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
        self.products = []

    def get_page(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            print(f"Error while downloading {url}: {e}")
            return None

    def scrape_categories(self, soup=None, parent_name=""):
        print("Scraping categories")
        html = self.get_page(self.base_url)
        if not html:
            return
        
        soup = BeautifulSoup(html, 'html.parser')
        categories = []

        menu_container = soup.select_one("div.innerbox ul.standard")
        if not menu_container:
            print("Category container not found.")
            return []

        for li in menu_container.select("li[id^='category_']"):
            a_tag = li.find("a")
            if not a_tag:
                continue
            href = a_tag.get("href")
            name = a_tag.get_text(strip=True)
            full_name = f"{parent_name} > {name}" if parent_name else name
            full_url = urljoin(self.base_url, href)
            categories.append((full_name, full_url))
            sub_ul = li.find("ul")
            if sub_ul:
                sub_categories = self.scrape_categories(BeautifulSoup(str(sub_ul), 'html.parser'), full_name)
                categories.extend(sub_categories)
        return categories

    def scrape_products_from_category(self, category_url, parent_category = None):
        print("Scraping products from category:", parent_category)
        html = self.get_page(category_url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        
        product_links = set()
        for a in soup.select("a.product-name, .product-item a, .product a, .product-link"):
            href = a.get("href")
            if href and "/pl/p/" in href:
                product_links.add(urljoin(self.base_url, href))

        for product_url in product_links:
            self.scrape_product(product_url, parent_category)
            time.sleep(0.5)

        pagination = soup.select("div.floatcenterwrap ul.paginator li a")
        next_page_url = None
        for a in pagination:
            if a.get_text(strip=True) == "»":  # next page arrow
                next_page_url = urljoin(self.base_url, a["href"])
                break
        if next_page_url:
            self.scrape_products_from_category(next_page_url, parent_category)
        
        #subcategories
        for sub_li in soup.select("li[id^='category_'] ul.level_1 li a"):
            sub_href = sub_li.get("href")
            sub_name = sub_li.get_text(strip=True)
            if sub_href and sub_href.startswith("/pl/"):
                sub_url = urljoin(self.base_url, sub_href)
                self.scrape_products_from_category(sub_url, parent_category=sub_name)

    def scrape_product(self, product_url, category_name):
        print("Scraping product:", product_url)
        html = self.get_page(product_url)
        if not html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        
        name = soup.select_one("h1[itemprop='name']")
        name = name.text.strip() if name else "N/A"
        
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
            "categories": set(),
            "url": product_url
        }

        if category_name:
            product_data["categories"].add(category_name)

        for existing in self.products:
            if existing["url"] == product_url:
                existing["categories"].update(product_data["categories"])
                return
        
        self.products.append(product_data)

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
        csv_path = os.path.join(self.output_folder, "products.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Name", "Price", "Description", "Image URLs", "Categories", "URL"])

            for product in self.products:
                writer.writerow([
                    product["name"],
                    product["price"],
                    product["description"],
                    ",".join(product["images"]),
                    "|".join(product["categories"]),
                    product["url"]
                ])        

    def scrape(self):
        start_time = time.time()
        print("Started Scraping")
        categories = self.scrape_categories()
        for category_name, category_url in categories:
            print("Category:", category_name)
            self.scrape_products_from_category(category_url, parent_category = category_name)
        self.save_to_csv()
        end_time = time.time()
        print(f"\nScraping took {end_time - start_time:.2f} seconds")
        print("Scraping completed. Data saved to", self.output_folder)

def main():
    scraper = WebScraper()
    scraper.scrape()
if __name__ == "__main__":
    main()