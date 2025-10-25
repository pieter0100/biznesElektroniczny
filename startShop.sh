#!/bin/bash

echo "Starting prestashop"

# start docker images
docker-compose up -d

# load sql dump
docker-compose exec -T mysql mysql -u root -p"admin" prestashop < ./prestashop/dbdata/sqlDump.sql