from common import *

from functions.dodanieProduktowPrzezWyszukiwarke import (
    dodanie_produktow_przez_wyszukiwarke,
)
from functions.pobranieFakturyVAT import pobierz_fakture
from functions.rejestracja import testowanie_rejestracji
from functions.sprawdzenieStatusuZamowienia import status_zamowienia
from functions.usuniecieProduktow import usun_produkty
from functions.wykonanieZamowienia import wykoanie_zamowienia

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)


# testowanie_rejestracji(driver)
# phrase = input("co wyszukac:")
# phrase = "nab"
# dodanie_produktow_przez_wyszukiwarke(driver, phrase)
usun_produkty(driver)
#
# while True:
#     akcja = input("Wybierz akcje:")
#
#     if akcja == "1":
#         testowanie_rejestracji(driver)
#     elif akcja == "2":
#         phrase = input("co wyszukac:")
#         dodanie_produktow_przez_wyszukiwarke(driver, phrase)
#     elif akcja == "3":
#         usun_produkty(driver)
#     elif akcja == "4":
#         wykoanie_zamowienia(driver)
#     elif akcja == "5":
#         status_zamowienia(driver)
#     elif akcja == "6":
#         pobierz_fakture(driver)
