from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import random
from faker import Faker

from functions.rejestracja import testowanie_rejestracji

fake = Faker("pl_PL")

# Tworzenie obiektu opcji
chrome_options = Options()

# argumenty ignorujących błędy SSL
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-ssl-errors")

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://localhost:8443/")


testowanie_rejestracji(driver)
