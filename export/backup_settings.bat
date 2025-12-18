@echo off
set CONTAINER=some-mysql
set DB_NAME=prestashop
set DB_USER=root
set DB_PASS=admin
set OUTPUT_FILE=prestashop_settings.sql

echo [PROCES] Eksportowanie ustawien bazy danych...

docker exec %CONTAINER% mysqldump -u%DB_USER% -p%DB_PASS% %DB_NAME% ps_configuration ps_shop_url ps_hook_module ps_contact ps_contact_lang ps_meta ps_meta_lang > %OUTPUT_FILE%

if %ERRORLEVEL% EQU 0 (
    echo [SUKCES] Plik %OUTPUT_FILE% zostal utworzony.
) else (
    echo [BLAD] Cos poszlo nie tak. Sprawdz czy kontener %CONTAINER% dziala.
)
pause