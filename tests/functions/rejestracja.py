from selenium import webdriver
import random
from faker import Faker
from selenium.webdriver.common.by import By
from time import sleep


def testowanie_rejestracji(driver: webdriver):
    fake = Faker("pl_PL")

    driver.get("https://localhost:8443/logowanie?create_account=1")

    gender_radio_button = driver.find_element(
        By.CSS_SELECTOR, f"input#field-id_gender-{random.randint(1, 2)}"
    )
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
    birthday_input.send_keys(
        f"{random.randint(1960,2005)}-{random.randint(0,12)}-{random.randint(1,27)}"
    )

    newsletter_checkbox = driver.find_element(By.NAME, "optin")
    newsletter_checkbox.click()

    customer_privacy_checkbox = driver.find_element(By.NAME, "customer_privacy")
    customer_privacy_checkbox.click()

    psgdpr_checkbox = driver.find_element(By.NAME, "psgdpr")
    psgdpr_checkbox.click()

    sleep(2)

    submit_button = driver.find_element(By.CSS_SELECTOR, ".form-control-submit")
    submit_button.click()
