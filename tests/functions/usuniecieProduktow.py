from common import *


def usun_produkty(driver):
    driver.get("https://localhost:8443/")

    bestsellers_grid = driver.find_element(By.CSS_SELECTOR, "div[data-id='ybpuyfk']")
    bestsellers_grid = bestsellers_grid.find_element(By.CSS_SELECTOR, ".slick-track")

    products = bestsellers_grid.find_elements(By.CSS_SELECTOR, ".slick-slide")[:3]

    # dodanie do koszyka
    for product in products:
        add_to_cart_button = product.find_element(
            By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"
        )
        driver.execute_script("arguments[0].click();", add_to_cart_button)

        sleep(0.5)

        go_to_summary_element = driver.find_element(
            By.CSS_SELECTOR, "button[data-dismiss='modal']"
        )
        driver.execute_script("arguments[0].click();", go_to_summary_element)

    driver.get("https://localhost:8443/koszyk?action=show")
    sleep(0.5)

    while True:
        try:
            cart_items = driver.find_element(By.CLASS_NAME, "cart-items")
        except Exception as e:
            print("brak produktow")
            break

        items = cart_items.find_elements(By.CLASS_NAME, "cart-item")

        if len(items) == 0:
            break

        try:
            remove_item = cart_items.find_element(By.CLASS_NAME, "remove-from-cart")
            driver.execute_script("arguments[0].click();", remove_item)
            sleep(0.5)

        except Exception as e:
            print(f"blad")
