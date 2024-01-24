#!/bin/sh
python webgen.py $1
xdg-open index.html
while true; do python webgen.py $1; sleep 1s; done
