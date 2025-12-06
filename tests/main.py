from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import random
from faker import Faker

fake = Faker('pl_PL')

# Tworzenie obiektu opcji
chrome_options = Options()

# argumenty ignorujących błędy SSL
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-ssl-errors")

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://localhost:8443/")

def testowanie_rejestracji():
    driver.get("https://localhost:8443/logowanie?create_account=1")

    gender_radio_button = driver.find_element(By.CSS_SELECTOR, f"input#field-id_gender-{random.randint(1, 2)}")
    gender_radio_button.click()

    firstname_input = driver.find_element(By.CSS_SELECTOR, "input#field-firstname")
    firstname_input.clear()
    firstname_input.send_keys(fake.first_name())

    surname_input = driver.find_element(By.CSS_SELECTOR, "input#field-lastname")
    surname_input.clear()
    surname_input.send_keys(fake.last_name())

    email_input = driver.find_element(By.CSS_SELECTOR, "input#field-email")
    email_input.clear()
    email_input.send_keys(fake.email())

    password_input = driver.find_element(By.CSS_SELECTOR, "input#field-password")
    password_input.clear()
    password_input.send_keys(fake.password())

    birthday_input = driver.find_element(By.CSS_SELECTOR, "input#field-birthday")
    birthday_input.clear()
    birthday_input.send_keys(f"{random.randint(1960,2005)}-{random.randint(0,12)}-{random.randint(1,27)}")

    newsletter_checkbox = driver.find_element(By.NAME, "optin")
    newsletter_checkbox.click()

    customer_privacy_checkbox = driver.find_element(By.NAME, "customer_privacy")
    customer_privacy_checkbox.click()

    psgdpr_checkbox = driver.find_element(By.NAME, "psgdpr")
    psgdpr_checkbox.click()

    sleep(2)

    submit_button = driver.find_element(By.CSS_SELECTOR, ".form-control-submit")
    submit_button.click()

testowanie_rejestracji()
# while(True):
#     print("wybierz akcje")
#     akcja = input()

#     if akcja == "1":
#         testowanie_rejestracji()

# if __name__ == "__main__":
#     print("test")