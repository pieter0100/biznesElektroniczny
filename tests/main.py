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
    driver.quit()


# --- WYKONANIE TESTÓW ---

# 1. Rejestracja
uruchom_test(testowanie_rejestracji)

# 2. Dodawanie przez wyszukiwarkę
phrase = "nab"
uruchom_test(dodanie_produktow_przez_wyszukiwarke, phrase)

# 3. Usuwanie produktów
uruchom_test(usun_produkty)

# 4. Wykonanie zamówienia
uruchom_test(wykoanie_zamowienia)

# 5. Status zamówienia
uruchom_test(status_zamowienia)

# 6. Pobranie faktury
uruchom_test(pobierz_fakture)

# 7. Dodanie z kategorii
uruchom_test(dodaj_do_koszyka_z_kategori)

