from common import *


def dodaj_do_koszyka_produkty(driver):
    driver.get("https://localhost:8443/")

    lista_prdoutkow = driver.find_element(By.CSS_SELECTOR, "section[data-id='ndq3cnv']")
    lista_prdoutkow = lista_prdoutkow.find_element(
        By.CSS_SELECTOR, ".slick-slide.slick-current.slick-active.first-active"
    )

    products = lista_prdoutkow.find_elements(By.CSS_SELECTOR, ".slick-slide1")

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
    sleep(1)

    make_order_button = driver.find_element(
        By.CSS_SELECTOR, "a[href='https://localhost:8443/zamówienie']"
    )
    make_order_button.click()


def formularz_konta(driver: webdriver):
    wait = WebDriverWait(driver, 10)
    fake = Faker("pl_PL")

    gender_id = random.randint(1, 2)
    gender_radio_button = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input#field-id_gender-{gender_id}")
        )
    )
    driver.execute_script("arguments[0].click();", gender_radio_button)

    firstname_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-firstname"))
    )
    firstname_input.clear()
    firstname_input.send_keys(fake.first_name())

    surname_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-lastname"))
    )
    surname_input.clear()
    surname_input.send_keys(fake.last_name())

    email_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-email"))
    )
    email_input.clear()
    email_input.send_keys(fake.email())

    # password_input = wait.until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-password"))
    # )
    # password_input.clear()
    # password_input.send_keys(fake.password())

    birthday_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-birthday"))
    )
    birthday_input.clear()
    birthday_input.send_keys(
        f"{random.randint(1960, 2005)}-{random.randint(1, 12)}-{random.randint(1, 27)}"
    )

    newsletter_checkbox = driver.find_element(By.NAME, "optin")
    newsletter_checkbox.click()

    customer_privacy_checkbox = driver.find_element(By.NAME, "customer_privacy")
    customer_privacy_checkbox.click()

    psgdpr_checkbox = driver.find_element(By.NAME, "psgdpr")
    psgdpr_checkbox.click()

    submit_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".continue.btn.btn-primary.float-xs-right")
        )
    )
    submit_button.click()


def formularz_wysylki(driver):
    fake = Faker("pl_PL")

    adress = driver.find_element(By.CSS_SELECTOR, "input[name='address1']")
    adress.clear()
    adress.send_keys("testowa 10")

    postcode = driver.find_element(By.CSS_SELECTOR, "input#field-postcode")
    postcode.clear()
    postcode.send_keys(fake.postcode())

    city = driver.find_element(By.CSS_SELECTOR, "input#field-city")
    city.clear()
    city.send_keys(fake.city())

    sleep(2)
    submit = driver.find_element(By.CSS_SELECTOR, "button[name='confirm-addresses']")
    submit.click()


def formualrz_dostawa(driver):
    fake = Faker("pl_PL")

    delivery_options_grid = driver.find_element(By.CLASS_NAME, "delivery-options")

    delivery_options_list = delivery_options_grid.find_elements(
        By.CSS_SELECTOR, ".delivery-option.js-delivery-option"
    )

    delivery_option = random.choice(delivery_options_list)
    delivery_option = delivery_option.find_element(
        By.CSS_SELECTOR, "input[type='radio']"
    )
    delivery_option.click()

    sleep(1)

    driver.find_element(By.CSS_SELECTOR, "button[name='confirmDeliveryOption']").click()


def formualrz_platnosc(driver):
    # platnosc przelewem
    driver.find_element(By.CSS_SELECTOR, f"input#payment-option-{2}").click()
    sleep(0.5)
    # warunki swiadzeni uslug
    driver.find_element(
        By.CSS_SELECTOR, "input[name='conditions_to_approve[terms-and-conditions]']"
    ).click()
    sleep(0.5)

    # zloz zamownie
    confirm_button = driver.find_element(By.CSS_SELECTOR, "div#payment-confirmation")
    confirm_button = confirm_button.find_element(By.CSS_SELECTOR, "button")
    confirm_button.click()

    sleep(2)


def wykoanie_zamowienia(driver):
    driver.get("https://localhost:8443/")

    dodaj_do_koszyka_produkty(driver)

    formularz_konta(driver)

    formularz_wysylki(driver)

    formualrz_dostawa(driver)

    formualrz_platnosc(driver)
