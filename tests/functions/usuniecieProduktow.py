from common import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


def usun_produkty(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:8443/")

    slider_section = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "section[data-id='ndq3cnv']")
        )
    )

    active_slide = slider_section.find_element(
        By.CSS_SELECTOR, ".slick-slide.slick-current.slick-active"
    )

    products = active_slide.find_elements(By.CSS_SELECTOR, ".slick-slide1")

    for product in products:
        add_to_cart_button = product.find_element(
            By.CSS_SELECTOR, "button[data-button-action='add-to-cart']"
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
        driver.execute_script("arguments[0].click();", add_to_cart_button)

        continue_shopping_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn-secondary[data-dismiss='modal']")
            )
        )
        continue_shopping_btn.click()

        wait.until(EC.invisibility_of_element_located((By.ID, "blockcart-modal")))

    driver.get("https://localhost:8443/koszyk?action=show")

    wait.until(EC.presence_of_element_located((By.ID, "main")))

    while True:
        try:
            wait_short = WebDriverWait(driver, 3)

            remove_button = wait_short.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "remove-from-cart"))
            )

            driver.execute_script("arguments[0].click();", remove_button)

            wait.until(EC.staleness_of(remove_button))

        except TimeoutException:
            print("Brak przycisków usuwania - koszyk jest pusty.")
            break
        except StaleElementReferenceException:
            continue
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
            break
