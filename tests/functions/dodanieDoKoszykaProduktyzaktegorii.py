from selenium.common import TimeoutException, ElementNotInteractableException

from common import *


def pobierz_linki_do_produktow(driver, product_elements):
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
            href_string = url.get_attribute("href")
            urls.append(href_string)


    return urls

def dodaj_z_kategori(driver):
    wait = WebDriverWait(driver, 10)

    products_section = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//section[@id='products-list']"))
    )

    product_elements = products_section.find_elements(
        By.XPATH, ".//article[contains(@class, 'product-miniature')]"
    )

    # get links
    urls = pobierz_linki_do_produktow(driver, product_elements)

    ilosc_produktow = 0

    for link in urls:
        if ilosc_produktow == 6:
            break

        driver.get(link)
        ilosc_produktu = random.randint(1, 2)

        plus_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.bootstrap-touchspin-up")
            )
        )

        czy_dodano_do_koszyka = False

        dostepnosc = driver.find_element(By.ID, "product-availability")
        tekst = dostepnosc.text
        if tekst != "":
            ilosc_produktu = 0

        for _ in range(ilosc_produktu):
            plus_button.click()


        try:
            add_to_cart_button = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
                )
            )
            add_to_cart_button.click()
            czy_dodano_do_koszyka = True

        except TimeoutException:
            print("zablokowany przycisk")
            czy_dodano_do_koszyka = False

        if czy_dodano_do_koszyka:
            ilosc_produktow += 1


def dodaj_do_koszyka_z_kategori(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(ROOT_URL)

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
    url = ROOT_URL + "/koszyk?action=show"
    driver.get(url)
    sleep(2)
