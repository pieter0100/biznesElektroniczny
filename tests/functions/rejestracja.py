from common import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def testowanie_rejestracji(driver: webdriver):
    # Inicjalizacja Explicit Wait (np. max 10 sekund oczekiwania)
    wait = WebDriverWait(driver, 10)
    fake = Faker("pl_PL")

    driver.get("https://localhost:8443/logowanie?create_account=1")

    # Czekamy, aż radio button będzie klikalny
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input#field-id_gender-{random.randint(1,2)}")
        )
    )
    gender_radio_button = driver.find_element(By.CSS_SELECTOR, f"input#field-id_gender-{random.randint(1,2)}")
    gender_radio_button.click()

    # Dla pól tekstowych czekamy na ich widoczność
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

    password_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-password"))
    )
    password_input.clear()
    password_input.send_keys(fake.password())

    birthday_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input#field-birthday"))
    )
    birthday_input.clear()
    # Poprawiłem zakres miesięcy na 1-12 (0 jest niepoprawny)
    birthday_input.send_keys(
        f"{random.randint(1960, 2005)}-{random.randint(1, 12)}-{random.randint(1, 27)}"
    )

    newsletter_checkbox = driver.find_element(By.NAME, "optin")
    newsletter_checkbox.click()

    customer_privacy_checkbox = driver.find_element(By.NAME, "customer_privacy")
    customer_privacy_checkbox.click()

    psgdpr_checkbox = driver.find_element(By.NAME, "psgdpr")
    psgdpr_checkbox.click()

    # Usunięto sleep(2) - wait.until przy submit wystarczy
    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-control-submit"))
    )
    submit_button.click()