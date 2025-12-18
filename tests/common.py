# Plik: common.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from time import sleep
import random
import string
from faker import Faker

# Możesz tu nawet wstępnie skonfigurować opcje Chrome!
from selenium.webdriver.chrome.options import Options

# Tworzenie obiektu opcji
chrome_options = Options()

# argumenty ignorujących błędy SSL
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-ssl-errors")
