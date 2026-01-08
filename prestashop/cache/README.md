# 📁 Struktura katalogu /cache

> ⚠️ **UWAGA:** Proszę nie usuwać plików `index.php` ani struktury katalogów znajdujących się w tym repozytorium.

## Dlaczego te pliki są w repozytorium?

Mimo że zawartość cache (wygenerowane pliki tymczasowe) jest ignorowana przez `.gitignore`, **sama struktura katalogów oraz pliki `index.php` muszą pozostać w repozytorium**.

Są one niezbędne do prawidłowego działania sklepu z dwóch powodów:

1.  🛡️ **Bezpieczeństwo:** Pliki `index.php` to tzw. "zaślepki". Blokują one możliwość podejrzenia zawartości katalogu przez przeglądarkę (Directory Listing). Bez nich każdy mógłby zobaczyć listę plików tymczasowych Twojego sklepu.
2.  🏗️ **Stabilność i Git:** Git nie śledzi pustych folderów. Aby PrestaShop miał gdzie zapisywać pliki cache (np. dla Smarty, TCPDF), foldery te muszą fizycznie istnieć. Pliki `index.php` wymuszają istnienie tych folderów w repozytorium.

## Co jest ignorowane?

Wszystkie pliki tymczasowe generowane przez sklep podczas jego działania (np. skompilowane szablony `.tpl.php`, tymczasowe pliki PDF) są automatycznie ignorowane przez plik `.gitignore` i nie zaśmiecają repozytorium.

## Wymagana struktura

Poniższa struktura plików jest oryginalna i wymagana przez PrestaShop:

```text
cache
├── cachefs/
├── purifier/
├── push/
├── sandbox/
├── smarty/
│   ├── cache/
│   └── compile/
└── tcpdf/