#!/bin/bash
CONTAINER="mysql"
DB_NAME="prestashop"
DB_USER="root"
DB_PASS="admin"
INPUT_FILE="prestashop_settings.sql"

echo "[OSTRZEŻENIE] Zamierzasz nadpisać ustawienia w bazie $DB_NAME."
read -p "Czy na pewno chcesz kontynuować? (t/n): " confirm

if [[ $confirm != [tTyY] ]]; then
    exit 1
fi

echo "[PROCES] Przywracanie danych..."
docker exec -i $CONTAINER mysql -u$DB_USER -p$DB_PASS $DB_NAME < $INPUT_FILE

if [ $? -eq 0 ]; then
    echo "[SUKCES] Ustawienia zostały przywrócone."
else
    echo "[BŁĄD] Wystąpił problem podczas importu."
fi