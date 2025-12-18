from selenium.common import TimeoutException

from common import *


def dodaj_z_kategori(driver):
    wait = WebDriverWait(driver, 10)

    products_section = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//section[@id='products-list']"))
    )

    product_elements = products_section.find_elements(
        By.XPATH, ".//article[contains(@class, 'product-miniature')]"
    )

    # get links
    urls = []
    for product_element in product_elements[1:6]:
        url = product_element.find_element(By.CSS_SELECTOR, ".img_block")
        url = url.find_element(By.CSS_SELECTOR, "a")
        href_string = url.get_attribute("href")
        urls.append(href_string)

    for link in urls:
        driver.get(link)
        ilosc_produktu = random.randint(1, 2)

        plus_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.bootstrap-touchspin-up")
            )
        )

        for _ in range(ilosc_produktu):
            plus_button.click()

            try:
                add_to_cart_button = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
                    )
                )
                add_to_cart_button.click()
            except TimeoutException:
                print("zablokowany przycisk")


def dodaj_do_koszyka_z_kategori(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:8443")

    # Czekanie na pojawienie się kontenera Elementora
    lista_kategorii = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class, 'elementor-column-wrap') and contains(@class, 'elementor-element-populated')]",
            )
        )
    )

    kategorie = lista_kategorii.find_elements(By.XPATH, "//li[@data-depth='0']")

    kategoria_1 = random.choice(kategorie)
    kategorie.pop(kategorie.index(kategoria_1))
    kategoria_1 = kategoria_1.find_element(By.CSS_SELECTOR, "a")
    kategoria_1 = kategoria_1.get_attribute("href")

    kategoria_2 = random.choice(kategorie)
    kategoria_2 = kategoria_2.find_element(By.CSS_SELECTOR, "a")
    kategoria_2 = kategoria_2.get_attribute("href")

    # idz do 1 kategorii
    driver.get(kategoria_1)

    dodaj_z_kategori(driver)

    # idz do 2 kategorii
    driver.get(kategoria_2)

    dodaj_z_kategori(driver)

    # pokaz koszyk
    sleep(1)
    driver.get("https://localhost:8443/koszyk?action=show")
    sleep(5)
