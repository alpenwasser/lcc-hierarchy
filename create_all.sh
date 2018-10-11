#!/usr/bin/env bash

[ -z "$1" ] && exit 1

for file in data/*json;do
    ./generate_category_tree.py "$file" "$1"
done
