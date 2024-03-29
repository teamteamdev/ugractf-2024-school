#!/usr/bin/env python3

import hmac
import random
import subprocess
import json
import sys
import os

PREFIX = "ugra_i_know_password_i_see_the_"
FLAG_SECRET = b"absent-copyright-lesson-plastic"
SUFFIX_SIZE = 12


def get_flag(user_id):
    return PREFIX + hmac.new(FLAG_SECRET, user_id.encode(), "sha256").hexdigest()[:SUFFIX_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    attachments = os.path.join(sys.argv[2], "attachments")
    flag = get_flag(user_id)

    subprocess.run(["./app/generate.sh", flag, attachments], check=True)

    json.dump({
        "flags": [flag]
    }, sys.stdout)


if __name__ == "__main__":
    generate()
