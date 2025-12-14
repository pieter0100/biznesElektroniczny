# Ręczny import danych do PrestaShop 1.7.8.11

## Generowanie danych

W katalogu `scraper` puść `main.py`

## Import kategori i produktów (bez zdjęć)

```Panel administracyjny > Konfiguruj > Zaawansowane > Importuj```

### Import kategorii

Wartości pól:

- Co chcesz zaimportować: **Kategorie** <br><br>
- Wybierz plik: `winohobby_data/categories.csv` 
- Język pliku: **Polski (Polish)**
- Separator pola: **;**
- Separator wielokrotnych wartości: **|** <br><br>
- Usuń wszystkie kategorie przed importem: **Tak**
- Pomiń ponowne generowanie minatur: **Nie**
- Wymuś wszystkie numery ID: **Tak**

Kliknij: ```Następny krok >```

- Zapisz swoje dane konfiguracji dopasowania: *Można nie trzeba*
- Wiersze do pominięcia: **1**

Wybierz nazwy kolumn odpowiadające tym w pliku (pamiętaj aby przeklikać strzałkami wyświetlonymi pod tabelką i przypisać nazwy wszystkim kolumnom)

Kliknij: ```Importuj```

### Import produktów

Wartości pól:

- Co chcesz zaimportować: **Produkty** <br><br>
- Wybierz plik: `winohobby_data/products.csv`
- Język pliku: **Polski (Polish)**
- Separator pola: **;**
- Separator wielokrotnych wartości: **|**<br><br>
- Usuń wszystkie produkty przed importem: **Tak**
- Użyć indeksu produktu jako klucza: **Nie**
- Pomiń ponowne generowanie minatur: **Nie**
- Wymuś wszystkie numery ID: **Nie**

Kliknij: ```Następny krok >```

- Zapisz swoje dane konfiguracji dopaswania: *Można nie trzeba*
- Wiersze do pominięcia: **1**

Wybierz nazwy kolumn odpowiadające tym w pliku (pamiętaj aby przeklikać strzałkami wyświetlonymi pod tabelką i przypisać nazwy wszystkim kolumnom)

Kliknij: ```Importuj```

## Import zdjęć do produktów

### Dodaj nowy klucz API

```Panel administracyjny > Konfiguruj > Zaawansowane > API```

Kliknij `Dodaj nowy klucz API`

Kliknij `Wygeneruj`
dodaj opis np. "import zdjęć"

Włącz klucz API: `TAK`

Uprawnienia:
- images: POST
- products: PUT

kliknij `Zapisz`

### Włącz API PrestaShop

```Panel administracyjny > Konfiguruj > Zaawansowane > API```

W sekcji Konfiguracja zaznacz:

Włącz API PrestaShop: `Tak`

Kliknij `Zapisz`

### Import zdjęć

Będąc w folderze `scraper` puść `bulk_add_images.py` uprzednio podmieniając klucz w pliku na ten nowy.