#!/bin/bash
pkill -f 'python /usr/lib/cgi-bin/daemon.py'

python /usr/lib/cgi-bin/daemon.py --port 8000 &
python /usr/lib/cgi-bin/daemon.py --port 8001 &
python /usr/lib/cgi-bin/daemon.py --port 8002 &
echo "Executando maquinas nas portas 8000, 8001 e 8002."
