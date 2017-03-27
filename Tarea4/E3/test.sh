#!/bin/bash
python3 router.py &
python3 worker0.py 1&
python3 worker1.py 2&
python3 worker2.py 3&
python3 client0.py &
python3 client1.py 