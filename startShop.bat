@echo off
echo Starting prestashop

:: Start docker images (w tle)
docker-compose up -d

:: Wait for containers to load (używamy komendy ping do symulacji sleep)
:: Pingujemy localhost 6 razy, czekając ok. 1 sekundę między pingami.
ping -n 6 127.0.0.1 >nul

:: Load sql dump
:: Używamy składni exec -T dla Docker Compose
docker-compose exec -T mysql mysql -u root -p"admin" prestashop < .\prestashop\dbdataDump\sqlDump.sql

echo Skrypt zakończony.