from common import *

from functions.dodanieProduktow import dodanie_produktow
from functions.rejestracja import testowanie_rejestracji
from functions.usuniecieProduktow import usun_produkty

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)


while True:
    akcja = input("Wybierz akcje:")

    if akcja == "1":
        testowanie_rejestracji(driver)
    elif akcja == "2":
        phrase = input("co wyszukac:")
        dodanie_produktow(driver, phrase)
    elif akcja == "3":
        usun_produkty(driver)
