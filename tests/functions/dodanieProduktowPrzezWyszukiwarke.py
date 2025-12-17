from common import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def dodanie_produktow_przez_wyszukiwarke(driver: webdriver, search_phrase: str):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:8443/")

    search_bar = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "pos-search__input"))
    )
    search_bar.clear()
    search_bar.send_keys(search_phrase, Keys.ENTER)

    try:
        products = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".item-product"))
        )
    except:
        print("Brak produktów w wyszukaniu lub timeout")
        return

    random_product = random.choice(products)

    add_to_cart_button = random_product.find_element(
        By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"
    )
    driver.execute_script("arguments[0].click();", add_to_cart_button)

    continue_shopping_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Kontynuuj zakupy')]")
        )
    )
    continue_shopping_button.click()

    go_to_summary_element = driver.find_element(
        By.CSS_SELECTOR, "a[href='//localhost:8443/koszyk?action=show']"
    )
    driver.execute_script("arguments[0].click();", go_to_summary_element)

    sleep(3)
