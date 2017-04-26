#!/bin/sh -u

find "Book Files" test_data/ -type f -name "*.txt" | parallel -j2 python3 ./gen_pos.py

#SAVEIFS=$IFS
#IFS=$(echo -en "\n\b")

#files=$(ls "Book Files"/*.txt test_data/*.txt)

##for i in $(find "Book Files" test_data/ -name "*.txt")
#find "Book Files" test_data/ -type f -name "*.txt" | while read fname
#do
    #echo "$fname"
    #python3 gen_pos.py "$fname"
#done

#IFS=$SAVEIFS

#cd "Book Files"
#for i in *.txt; do python3 ../gen_pos.py "$i"; done
#cd ../
#cd test_data/
#for i in *.txt; do python3 ../gen_pos.py "$i"; done
