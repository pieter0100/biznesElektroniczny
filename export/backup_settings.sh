#!/bin/bash
CONTAINER="some-mysql"
DB_NAME="prestashop"
DB_USER="root"
DB_PASS="admin"
OUTPUT_FILE="prestashop_settings.sql"

echo "[PROCES] Eksportowanie ustawień z kontenera Docker..."

docker exec $CONTAINER mysqldump -u$DB_USER -p$DB_PASS $DB_NAME ps_configuration ps_shop_url ps_hook_module ps_contact ps_contact_lang ps_meta ps_meta_lang > $OUTPUT_FILE

if [ $? -eq 0 ]; then
    echo "[SUKCES] Plik $OUTPUT_FILE został utworzony."
else
    echo "[BŁĄD] Sprawdź czy kontener $CONTAINER działa."
fi