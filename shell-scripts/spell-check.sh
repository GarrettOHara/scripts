#!/bin/zsh
echo "pass path of file as CLI arg"

for f in *; do 
    echo $f
    aspell list < $f | sort | uniq -c
done

echo "Please correct misspelled words..."

for f in *; do 
    aspell check $f
done

