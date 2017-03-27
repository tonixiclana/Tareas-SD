#!/bin/bash

python3 server.py &

python3 client.py spain &
python3 client.py spain &
python3 client.py england &
python3 client.py england &
python3 client.py mexico &
python3 client.py mexico 
