from common import *
from functions.dodanieDoKoszykaProduktyzaktegorii import dodaj_do_koszyka_z_kategori

from functions.dodanieProduktowPrzezWyszukiwarke import (
    dodanie_produktow_przez_wyszukiwarke,
)
from functions.pobranieFakturyVAT import pobierz_fakture
from functions.rejestracja import testowanie_rejestracji
from functions.sprawdzenieStatusuZamowienia import status_zamowienia
from functions.usuniecieProduktow import usun_produkty
from functions.wykonanieZamowienia import wykoanie_zamowienia, dodaj_do_koszyka_produkty


def uruchom_test(funkcja_testowa, *args):
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    funkcja_testowa(driver, *args)
    input()
    driver.quit()

def testy():
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    dodaj_do_koszyka_z_kategori(driver)

    phrase = "nab"
    dodanie_produktow_przez_wyszukiwarke(driver, phrase)

    usun_produkty(driver)

    testowanie_rejestracji(driver)

    wykoanie_zamowienia(driver)

# # 5. Status zamówienia
# uruchom_test(status_zamowienia)
#
# # 6. Pobranie faktury
# uruchom_test(pobierz_fakture)

testy()
input()
