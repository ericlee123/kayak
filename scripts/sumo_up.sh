~/Code/distributed/kayak/scripts/down.sh

python3 setup.py install >/dev/null 2>&1

zattd -c conf/node0.conf &
zattd -c conf/node1.conf &
zattd -c conf/node2.conf &
zattd -c conf/node3.conf &
zattd -c conf/node4.conf &
