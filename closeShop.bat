@echo off
echo Closing prestashop and creating SQL dump...

:: Tworzenie zrzutu SQL
:: W Batch musimy użyć operatora przekierowania >
docker-compose exec -T mysql mysqldump -u root -p"admin" prestashop > .\prestashop\dbdataDump\sqlDump.sql

echo SQL dump created successfully in .\prestashop\dbdataDump\sqlDump.sql

:: Zamykanie obrazów Docker
docker-compose down

echo Docker containers stopped.