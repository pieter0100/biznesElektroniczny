from common import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def dodanie_produktow_przez_wyszukiwarke(driver: webdriver, search_phrase: str):
    wait = WebDriverWait(driver, 10)
    driver.get(ROOT_URL)

    search_bar = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "pos-search__input"))
    )
    search_bar.clear()
    search_bar.send_keys(search_phrase, Keys.ENTER)

    products_section = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//section[@id='products-list']"))
    )

    product_elements = products_section.find_elements(
        By.XPATH, ".//article[contains(@class, 'product-miniature')]"
    )

    urls = []
    for product_element in product_elements:
        url = product_element.find_element(By.CSS_SELECTOR, ".img_block")

        flaga_produktu = product_element.find_element(By.CSS_SELECTOR, ".img_block")
        flaga_produktu = flaga_produktu.find_element(By.CSS_SELECTOR, ".product-flag")

        flaga_produktu = flaga_produktu.find_elements(By.XPATH, ".//*")
        if len(flaga_produktu) < 0:
            print("brak produktu")
        else:
            url = url.find_element(By.CSS_SELECTOR, "a")
            urls.append(url.get_attribute("href"))

    driver.get(random.choice(urls))

    try:
        add_to_cart_button = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
            )
        )
        add_to_cart_button.click()

    except Exception as e:
        pass
    print("zablokowany przycisk")
