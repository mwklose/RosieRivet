#!/bin/bash
base="test"
bumm="_expected.csv"
for i in 1 2 3 4 5 6 7
do
    python3 ../../src/RivetCLI.py -s test$i.csv
    diff -u -w out.csv $base$i$bumm
done
