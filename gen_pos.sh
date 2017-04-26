#!/bin/sh -u

#find "Book Files" test_data/ -type f -name "*.txt" | parallel -j2 python3 ./gen_pos.py

find "Book Files" test_data/ -type f -name "*.txt" | while read fname
do
    echo "$fname"
    python3 gen_pos.py "$fname"
done
