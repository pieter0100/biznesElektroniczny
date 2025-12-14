import requests
import os
import sys
import csv
import time
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
import threading

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Konfiguracja
PRESTASHOP_URL = "https://localhost:8443"  # PrestaShop URL
API_KEY = "LMD6FVVFQHEFLXULJUYYZJPDEQH9Y7R9"   # API Key
IMAGES_CSV_PATH = "winohobby_data/images.csv"  # Path to CSV with image map
IMAGES_FOLDER = "winohobby_data/images"        # Folder with images
MAX_THREADS = 5  # Reduced from 10 to avoid overwhelming PrestaShop

# Per-product locks to avoid concurrent uploads to the same product (which can race on directory/thumb creation)
_product_locks = {}
_product_locks_guard = threading.Lock()

def _get_product_lock(product_id: str) -> threading.Lock:
    with _product_locks_guard:
        if product_id not in _product_locks:
            _product_locks[product_id] = threading.Lock()
        return _product_locks[product_id]

def add_image_to_product(product_id, image_path):
    MAX_SIZE_BYTES = 3000 * 1024  # PrestaShop limit: 3000 KB
    
    if not os.path.exists(image_path):
        print(f"[ERROR] File does not exist: {image_path}")
        return False
    
    # Check file size before uploading
    file_size = os.path.getsize(image_path)
    if file_size > MAX_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        print(f"[SKIP] {os.path.basename(image_path)} - Too large ({size_mb:.2f} MB, max 3.0 MB)")
        return False
    
    # Verify file is a valid image and get actual format
    actual_format = None
    try:
        with open(image_path, 'rb') as f:
            header = f.read(12)
            # Check for JPEG magic bytes
            if header.startswith(b'\xff\xd8\xff'):
                actual_format = 'JPEG'
            elif header.startswith(b'\x89PNG'):
                actual_format = 'PNG'
            elif header.startswith(b'GIF'):
                actual_format = 'GIF'
            else:
                print(f"[FAIL] {os.path.basename(image_path)} - Invalid image format (corrupted or wrong extension) | Size: {file_size} bytes")
                return False
    except Exception as e:
        print(f"[FAIL] {os.path.basename(image_path)} - Cannot read file: {str(e)}")
        return False
    
    url = f"{PRESTASHOP_URL}/api/images/products/{product_id}"

    # Map actual format to proper MIME type
    mime_map = {
        'JPEG': 'image/jpeg',
        'PNG': 'image/png',
        'GIF': 'image/gif',
    }
    mime_type = mime_map.get(actual_format, 'application/octet-stream')
    
    # Avoid racing concurrent uploads to the same product (directory/thumb generation)
    product_lock = _get_product_lock(str(product_id))
    with product_lock:
        attempts = 0
        max_attempts = 3
        backoff_base = 1.5
        last_timeout = None
        while attempts < max_attempts:
            attempts += 1
            try:
                # Sending image as multipart/form-data with longer timeout for large files
                timeout = max(60, (file_size // (1024 * 1024)) + 30)  # At least 60s, plus ~1s per MB
                last_timeout = timeout
                with open(image_path, 'rb') as f:
                    files = {
                        'image': (os.path.basename(image_path), f, mime_type)
                    }
                    response = requests.post(
                        url,
                        auth=HTTPBasicAuth(API_KEY, ""),
                        files=files,
                        verify=False,
                        timeout=timeout
                    )

                # Accept 200, 201 and 500 with PHP Notice
                if response.status_code in [200, 201]:
                    print(f"[OK] {os.path.basename(image_path)} ({actual_format}, {file_size} bytes)")
                    return True
                elif response.status_code == 500 and "PHP Notice" in response.text:
                    print(f"[OK] {os.path.basename(image_path)} (PHP Notice)")
                    return True
                else:
                    # If first try fails with code 76 or transient 5xx, retry with backoff
                    body_snippet = ""
                    try:
                        body_snippet = response.text[:700]
                    except Exception:
                        body_snippet = ""

                    if response.status_code in (500,) or "<![CDATA[76]]>" in body_snippet or "Error while creating image" in body_snippet:
                        if attempts < max_attempts:
                            sleep_s = (backoff_base ** attempts)
                            print(f"[RETRY] {os.path.basename(image_path)} - attempt {attempts}/{max_attempts} after {sleep_s:.1f}s (status {response.status_code})")
                            time.sleep(sleep_s)
                            continue
                    # Non-retriable or exhausted
                    print(f"[FAIL] {os.path.basename(image_path)} - Product ID: {product_id}, Status: {response.status_code}, Size: {file_size} bytes, Format: {actual_format}")
                    if response.status_code >= 400:
                        try:
                            error_text = response.text[:700]
                            if "error" in error_text.lower() or "exception" in error_text.lower() or "message" in error_text.lower():
                                print(f"  Details: {error_text}")
                        except Exception:
                            pass
                    return False

            except requests.exceptions.Timeout:
                if attempts < max_attempts:
                    sleep_s = (backoff_base ** attempts)
                    print(f"[TIMEOUT] {os.path.basename(image_path)} - retry {attempts}/{max_attempts} after {sleep_s:.1f}s (timeout {last_timeout}s)")
                    time.sleep(sleep_s)
                    continue
                print(f"[TIMEOUT] {os.path.basename(image_path)} - Upload took too long (timeout after {last_timeout}s)")
                return False
            except requests.exceptions.ConnectionError:
                if attempts < max_attempts:
                    sleep_s = (backoff_base ** attempts)
                    print(f"[CONN_ERR] {os.path.basename(image_path)} - retry {attempts}/{max_attempts} after {sleep_s:.1f}s")
                    time.sleep(sleep_s)
                    continue
                print(f"[CONN_ERR] {os.path.basename(image_path)} - Connection error to PrestaShop")
                return False
            except Exception as e:
                print(f"[FAIL] {os.path.basename(image_path)} - Exception: {str(e)}")
                return False

def main():
    if not os.path.exists(IMAGES_CSV_PATH):
        print(f"\nError: File does not exist: {IMAGES_CSV_PATH}")
        return False
    
    if not os.path.exists(IMAGES_FOLDER):
        print(f"\nError: Folder does not exist: {IMAGES_FOLDER}")
        return False
    
    products_with_images = []
    try:
        with open(IMAGES_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            header = next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    product_id = row[0].strip()
                    # All columns after the first are image filenames
                    image_names = [img.strip() for img in row[1:] if img.strip()]
                    if product_id and image_names:
                        products_with_images.append((product_id, image_names))
    except Exception as e:
        print(f"\nError reading CSV: {e}")
        return False
    
    print(f"\nFound {len(products_with_images)} products with images")
    
    # Prepare all upload tasks
    upload_tasks = []
    for product_id, image_names in products_with_images:
        for image_name in image_names:
            image_path = os.path.join(IMAGES_FOLDER, image_name)
            upload_tasks.append((product_id, image_path, image_name))
    
    print(f"Total images to upload: {len(upload_tasks)}")
    print(f"Using {MAX_THREADS} concurrent threads")
    sys.stdout.flush()
    
    # Upload with threading
    successful = 0
    failed = 0
    
    start_time = time.time()
    try:
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(add_image_to_product, product_id, image_path): (product_id, image_name)
                for product_id, image_path, image_name in upload_tasks
            }
            
            # Process results as they complete
            completed = 0
            for future in as_completed(future_to_task):
                product_id, image_name = future_to_task[future]
                try:
                    result = future.result()
                    if result:
                        successful += 1
                    else:
                        failed += 1
                except Exception as e:
                    print(f"Error uploading {image_name}: {e}")
                    failed += 1
                
                completed += 1
                if completed % 10 == 0:
                    print(f"Progress: {completed}/{len(upload_tasks)} - Success: {successful}, Failed: {failed}")
                    sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Upload cancelled by user")
        sys.stdout.flush()
    
    elapsed_time = time.time() - start_time
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total images: {len(upload_tasks)}")
    print(f"Successfully uploaded: {successful}")
    print(f"Failed uploads: {failed}")
    print(f"Success rate: {successful/len(upload_tasks)*100:.1f}%")
    print(f"Time taken: {elapsed_time:.1f} seconds")
    
    if failed == 0:
        print("\nAll products have been updated!")
        return True
    else:
        print(f"\n  {failed} images had issues")
        return successful > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)