echo "Encendiendo clientes..."
python3 slave0.py &
python3 slave1.py &
python3 slave2.py &
python3 slave3.py &
sleep 2
echo "Encendiendo servidor.."
python3 master.py
sleep 1