#!/bin/sh
PATH=/Users/hongzhang/Documents/GitHub/IntelligentKYC/datacache/*.json
rm $PATH

* * 2 * * python3 do_scrape.py --special_search=Chase
* * 2 * * python3 do_scrape.py --special_search=Amex
* * 2 * * python3 do_scrape.py --special_search=Citi
* * 2 * * python3 do_scrape.py

