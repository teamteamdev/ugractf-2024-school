#!/usr/bin/env python3

from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag

import PIL.Image, PIL.ImageFont, PIL.ImageDraw
import gzip
import io
import os
import random
import re


BATCH_RE = re.compile(b"<(d|k)(\d\d\d\d\d)>")


def generate():
    flag = get_flag()
    random.seed(int(flag.replace("_", ""), 36)) 
    

    bio = io.BytesIO()
    img = PIL.Image.new("RGB", (384, 24), (64, 64, 64))
    draw = PIL.ImageDraw.ImageDraw(img)
    font = PIL.ImageFont.load(os.path.join("private", "ter-u14b_iso-8859-1.pil"))
    draw.text((16, 5), flag, font=font, fill=(255, 211, 100))
    img = img.resize((1448, 90))
    img.save(bio, format="BMP")

    key = random.randbytes(524288)
    data = (bio.getvalue() + b"\0" * 524288)[:524288]
    data_enc = bytes(a ^ b for a, b in zip(key, data))


    raw_data = open(os.path.join("private", "template.img"), "rb").read()
    P_OFFSET = 47185408
   
    with gzip.open(os.path.join(get_attachments_dir(), "harddisk.img.gz"), "wb", compresslevel=1) as f_img:
        f_img.write(raw_data[:P_OFFSET])
        for i in range(P_OFFSET, len(raw_data), 8):
            chunk = raw_data[i:i + 8]
            if (m := BATCH_RE.match(chunk)):
                offset = int(m.group(2)) * 8
                f_img.write((data_enc if m.group(1) == b"d" else key)[offset:offset + 8])
            else:
                f_img.write(chunk)


if __name__ == "__main__":
    generate()
