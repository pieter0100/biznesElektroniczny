from config import *
import requests
from http import HTTPStatus
from requests.auth import HTTPBasicAuth
from io import BytesIO
import xml.etree.ElementTree as ET
import json
from concurrent.futures import ThreadPoolExecutor


PRODUCT_QUANTITY = 5
PRODUCT_WEIGHT = 0.1
NUMBER_OF_PRODUCTS_TO_IMPORT = -1 # -1 means all products
IMAGE_BASE_URL = ""

def get_image_data(image_name):
    local_path_images = os.path.join(SCRAPING_RESULST_DIRECTORY, "images", image_name)
    print(local_path_images)
    if os.path.exists(local_path_images):
        log_message(f"Loading local image: {local_path_images}")
        with open(local_path_images, 'rb') as f:
            return BytesIO(f.read())
            
    if os.path.exists(local_path_images):
        log_message(f"Loading local image: {local_path_images}")
        with open(local_path_images, 'rb') as f:
            return BytesIO(f.read())

    if IMAGE_BASE_URL:
        full_url = IMAGE_BASE_URL + image_name
        try:
            response = requests.get(full_url, verify=False, timeout=10)
            if response.status_code == 200:
                log_message(f"Downloaded image from {full_url}")
                return BytesIO(response.content)
            else:
                log_message(f"Failed to download image {full_url}: {response.status_code}")
        except Exception as e:
            log_message(f"Error downloading image {full_url}: {str(e)}")
            
    log_message(f"Image not found locally nor downloadable: {image_name}")
    return None


def upload_product_image(product_id, product_name, product_image):
    product_image_data = get_image_data(product_image)
    if not product_image_data:
        return
    upload_url = f"{PRODUCTS_IMAGES_URL}/{product_id}"
    
    files = {'image': (product_image, product_image_data, 'image/jpeg')}

    try:
        response = requests.post(
            upload_url,
            files=files,
            auth=HTTPBasicAuth(API_KEY, ''),
            verify=False
        )

        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            log_message(f"Image uploaded for product {product_name} successfully!")
        else:
            log_message(f"Failed to upload image for product {product_name}: {response.status_code} {response.text}")
    except Exception as e:
        log_message(f"Exception uploading image for {product_name}: {str(e)}")

def get_stock_id(product_id):
    
    response = requests.get(
        f"{STOCK_AVAILABLES_URL}?filter[id_product]={product_id}",
        auth=(API_KEY, ''),
        verify=False
    )
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        stock_ids = [node.attrib['id'] for node in root.findall(".//stock_available")]
        return stock_ids[0] if stock_ids else None
    else:
        raise Exception(f"Error fetching stock ID: {response.content}")


def update_stock(stock_id, quantity):

    response = requests.get(f"{STOCK_AVAILABLES_URL}/{stock_id}", auth=(API_KEY, ''), verify=False)
    if response.status_code == HTTPStatus.OK:
        # Fetch product stock data and modify its quantity
        stock_data = ET.fromstring(response.content)
        for node in stock_data.findall(".//quantity"):
            node.text = str(quantity)
        
        update_response = requests.put(
            f"{STOCK_AVAILABLES_URL}/{stock_id}",
            auth=(API_KEY, ''),
            data=ET.tostring(stock_data),
            headers=POST_HEADERS,
            verify=False
        )
        
        if update_response.status_code in [200, 204]:
            log_message(f"Stock updated successfully for stock ID {stock_id}")
        else:
            raise Exception(f"Error updating stock: {update_response.content}")
    else:
        raise Exception(f"Error fetching stock data: {response.content}")


def create_product(product_json, categories_ids):
    
    product_name = product_json['name']
    product_price = product_json['offers'][0]['price']
    reference = product_json['properties'][0]['value']
    description = product_json['description']
    properties = ''

    
    for prop in product_json['properties']:
        properties += f'<br>{prop["type"]}: {prop["value"]} <br>'
    properties.strip()
    
    full_description = f'{description}<br>{properties}'
        
    product_netto_price = round(float(product_price) / 1.23, 6)

    product_xml = f"""<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
        <product>
            <id_category_default>2</id_category_default>
            <id_tax_rules_group>1</id_tax_rules_group>
            <price><![CDATA[{product_netto_price}]]></price>
            <new>0</new>
            <id_shop_default>1</id_shop_default>
            <weight><![CDATA[{PRODUCT_WEIGHT}]]></weight>
            <reference><![CDATA[{reference}]]></reference>
            <available_for_order>1</available_for_order>
            <active>1</active>
            <show_price>1</show_price>            
            <state>1</state>
            <name>
                <language id="1"><![CDATA[{product_name}]]></language>
            </name>
            <description>
                <language id="1"><![CDATA[{full_description}]]></language>
            </description>
            <associations>
                <categories>
                    <category>
                        <id>2</id>
                    </category>
    """
    
    """
            <description>
                <language id="1"><![CDATA[{properties}]]></language>
            </description>
    """
    # Iterate over categories and append them to the product_xml string
    for level, category_name in product_json['categories'].items():
        if level == "level4": # Prestashop categories page doesn't list deeper than level 3 categories
            break
        product_xml += f"""
            <category>
                <id><![CDATA[{categories_ids[category_name]}]]></id>
            </category>"""

    # Closing the XML structure
    product_xml += """
                </categories>
            </associations>
        </product>
    </prestashop>"""
        
    response = requests.post(PRODUCTS_URL, auth=(API_KEY, ''), headers=POST_HEADERS, data=product_xml.encode('utf-8'), verify=False)
    global log_file
    
    if response.status_code == HTTPStatus.CREATED:
        log_message(f"Product {product_name} created successfully!")
    else:
        log_message(f"Failed to create product {product_name}: {response.status_code}")
        log_message(response.text)
        return
        
        
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    product_id_element = root.find(".//id")
    product_id = product_id_element.text.strip()

    try:
        quantity = int(product_json.get('quantity', PRODUCT_QUANTITY))
    except (ValueError, TypeError):
        quantity = PRODUCT_QUANTITY

    with ThreadPoolExecutor() as executor:
        executor.submit(update_stock(get_stock_id(product_id), quantity))
        for image_link in product_json['images']:
            executor.submit(upload_product_image(product_id, product_name, image_link))


def create_products(products_data, categories_ids, max_products_count=-1):
    if max_products_count == -1:
        max_products_count = len(products_data)
    product_counter = max_products_count
    
    for product in products_data:
        create_product(product, categories_ids)
        product_counter -= 1
        if product_counter == 0:
            break
    
def load_to_memory_json_data():
    with open(SCRAPING_PRODUCTS_FILE, 'r', encoding='utf-8') as file:
        products_data = json.load(file)
        
    with open(CATEGORIES_IDS_OUTPUT_FILE, 'r', encoding='utf-8') as file_cat:
        categories_ids = json.load(file_cat)
        
    return products_data, categories_ids

sys.stdout.write("Importing products...\n")

products_data, categories_ids = load_to_memory_json_data()
create_products(products_data, categories_ids, max_products_count=NUMBER_OF_PRODUCTS_TO_IMPORT)

sys.stdout.write(f"\rImporting products finished\n")