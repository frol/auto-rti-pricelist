#!/bin/bash

if [ ! -f run ]; then
    exit 1
fi

. /www/price/env/bin/activate
python /www/price/project/transform.py
if [[ $? != 0 ]]; then
    mv price.csv price.csv.cp1251
    iconv -f cp1251 price.csv.cp1251 > price.csv
    rm price.csv.cp1251
    python /www/price/project/transform.py
fi
curl -s -T pricelist.html ftp://h2.prohosting.com.ua/www/price/ --user auto-rti:kd30JSkjd30dk5

rm run
