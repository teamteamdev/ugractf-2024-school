#!/bin/bash

tcpdump -vv -i eth0 -w /data/capture.pcap &
tpid=$!

# wait for server and tcpdump to start
sleep 1

python3 client.py

sleep 1
kill $tpid
wait $tpid
