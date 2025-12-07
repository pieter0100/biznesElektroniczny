from common import *


def dodanie_produktow(driver: webdriver, search_phrase: str):
    driver.get("https://localhost:8443/")

    search_bar = driver.find_element(By.CLASS_NAME, "pos-search__input")
    search_bar.clear()
    search_bar.send_keys(search_phrase, Keys.ENTER)

    product_grid = driver.find_element(By.CSS_SELECTOR, ".row.product_content.grid.row")

    # wait for products to load
    sleep(1)
    products = product_grid.find_elements(By.CSS_SELECTOR, ".item-product")
    if len(products) == 0:
        print("brak produktow w wyszukaniu")

    random_product = random.choice(products)

    add_to_cart_button = random_product.find_element(
        By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)

    sleep(3)

    go_to_summary_element = driver.find_element(
        By.CSS_SELECTOR, "a[href='//localhost:8443/koszyk?action=show']"
    )
    driver.execute_script("arguments[0].click();", go_to_summary_element)

    sleep(3)
