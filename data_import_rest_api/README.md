# Import Danych do PrestaShop REST API

## 1. Wymagana poprawka na serwerze
Bez tego import produktów wyrzuci błąd przy zdjęciach.
W pliku `/classes/Product.php` na serwerze PrestaShop znajdź funkcję `getCoverWs()` (ok. linii 7178) i zamień ją na:

```php
public function getCoverWs()
    {
        $result = $this->getCover($this->id);

        if (is_array($result) && isset($result['id_image'])) {
            return $result['id_image'];
        }

        return null;
    }
```

## 2. Konfiguracja

1. Puść `data_import_rest_api/setup.sh`
2. Ustaw nowy klucz API
    - Uprawnienia GET, PUT, POST dla Zasobów:
        - categories
        - images
        - products
        - stock_availables

    - w pliku `data_import_rest_api/.env` wpisz swoje dane
        ``` Ini
        API_KEY=TWOJ_KLUCZ_API_Z_PANELU
        API_URL=https://localhost:8443/api
        ```
3. Uruchom import -> `data_import_rest_api/run.sh`