#!/bin/bash

echo "Closing prestashop"

# create sql dump
docker-compose exec -T mysql mysqldump -u root -p"admin" prestashop > ./prestashop/dbdataDump/sqlDump.sql

# close docker images
docker-compose down

