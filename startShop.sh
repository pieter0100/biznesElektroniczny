#!/bin/bash

echo "Starting prestashop"

# start docker images
docker-compose up -d

# wait for containers to load
sleep 2s

# load sql dump
docker-compose exec -T mysql mysql -u root -p"admin" prestashop < ./prestashop/dbdataDump/sqlDump.sql