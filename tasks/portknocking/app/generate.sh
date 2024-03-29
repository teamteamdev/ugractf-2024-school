#!/usr/bin/env nix-shell
#!nix-shell -p docker-compose -p tcpreplay -p gnugrep -p gawk -p coreutils -i bash

set -e

# argument processing
export FLAG="$1"
workdir="$2"

# setting work directory and creating tmp dir
gendir="$(dirname "${BASH_SOURCE[0]}")"
cd "$gendir"

# generate suffix & project name
suffix="$(tr -dc a-z0-9 </dev/urandom 2>/dev/null | head -c 16)"
export COMPOSE_PROJECT_NAME=capture_$suffix

# docker start
trap "docker-compose down -t 1 >&2" INT TERM EXIT
docker-compose up -d --build server >&2
docker-compose logs -f server >&2 &
timeout 20 docker-compose up --build client >&2

# fix checksum in captured traffic
tcprewrite --fixcsum --infile "$TMPDIR/capture.pcap" --outfile="$workdir/capture.pcap"
