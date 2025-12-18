@echo off
set CONTAINER=some-mysql
set DB_NAME=prestashop
set DB_USER=root
set DB_PASS=admin
set INPUT_FILE=prestashop_settings.sql

echo [OSTRZEZENIE] Zamierzasz nadpisac ustawienia w bazie %DB_NAME%.
set /p confirm="Czy na pewno chcesz kontynuowac? (T/N): "
if /i "%confirm%" neq "T" exit

echo [PROCES] Przywracanie danych z pliku %INPUT_FILE%...

docker exec -i %CONTAINER% mysql -u%DB_USER% -p%DB_PASS% %DB_NAME% < %INPUT_FILE%

if %ERRORLEVEL% EQU 0 (
    echo [SUKCES] Ustawienia zostaly przywrocone.
) else (
    echo [BLAD] Wystapil problem podczas importu.
)
pause