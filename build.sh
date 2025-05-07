#!/bin/bash


URL="https://www.amfiindia.com/spages/NAVAll.txt"


curl -s $URL -o NAVAll.txt


awk 'BEGIN {OFS="\t"; print "Scheme Name", "Asset Value"} {print $1, $5}' NAVAll.txt > nav_data.tsv

echo "Data extracted and saved to nav_data.tsv"
