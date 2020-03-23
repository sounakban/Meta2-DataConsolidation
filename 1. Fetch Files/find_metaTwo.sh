#!/bin/bash

function loop() { 
    for i in "$1"/*
    do
        if [ -d "$i" ]; then
            loop "$i"
        elif [ -e "$i" ]; then
            if [ ${i: -4} == ".tsv" ]; then
                temp1=$(head -10 "$i" | grep -n "Meta-Two" | wc -c)
                temp2=$(head -10 "$i" | grep -n "Meta Two" | wc -c)
                if [ $temp1 -gt 1 -o $temp2 -gt 1 ]; then
                    echo "$i" >> MetaTwo_fileList.txt
                fi
            fi
        else
            echo "$i"" - Folder Empty"
        fi
    done
}

# rm MetaTwo_fileList.txt
touch MetaTwo_fileList.txt
loop "/mnt/hassServer/Active_Projects/Tetris/"

