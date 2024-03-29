#!/usr/bin/env sh
mkdir -p /state/markers

trap 'pkill -P $$; exit 0' EXIT INT TERM

python3 simulator.py /state "$SERVICE_HOST" &

# Reap orphans
wait
