from common import *

from functions.dodanieProduktowPrzezWyszukiwarke import (
    dodanie_produktow_przez_wyszukiwarke,
)
from functions.rejestracja import testowanie_rejestracji
from functions.usuniecieProduktow import usun_produkty
from functions.wykonanieZamowienia import wykoanie_zamowienia

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)


while True:
    akcja = input("Wybierz akcje:")

    if akcja == "1":
        testowanie_rejestracji(driver)
    elif akcja == "2":
        phrase = input("co wyszukac:")
        dodanie_produktow_przez_wyszukiwarke(driver, phrase)
    elif akcja == "3":
        usun_produkty(driver)
    elif akcja == "4":
        wykoanie_zamowienia(driver)
