#!/bin/bash
set -euo pipefail

secret='kjfjdse324j32098vjsk;'

user_id="$1"
workdir="$2"

attachments_dir="$workdir/attachments"
mkdir -p $attachments_dir

seed=$(echo "$user_id" | openssl dgst -hmac "$secret" | cut -d' ' -f2)
seed="0x${seed:0:8}"

cp /app/install_it "$attachments_dir/install_it"
hash=$(/app/patch_it "$attachments_dir/install_it" "$seed")
flag=$(/app/fast_flag "$attachments_dir/install_it" "$seed" "$hash")

echo "{\"flags\": [\"$flag\"]}"
