#!/usr/bin/python3
from io import BytesIO
from openlocationcode import openlocationcode
import sys
import piexif


def _merge(deg: (float, float), min: (float, float), sec: (float, float), ref: str):
    deg = deg[0] / (deg[1] or 1)
    min = min[0] / (min[1] or 1)
    sec = sec[0] / (sec[1] or 1)
    return (1 if ref in b"NE" else -1) * (deg + min/60 + sec/3600)


def _into_split(whole: float):
    return (int(whole // 1), 1), (int(whole % 1 * 60 // 1), 1), (int(whole % 1 * 60 % 1 * 60 * 100), 100)


def tag(image: bytes, lat: float, lon: float) -> bytes:
    exif_bytes = piexif.dump({"0th": {}, "1th": {}, "Exif": {}, "GPS": {
        0: (2, 0, 0, 0),
        1: "N" if lat >= 0 else "S",
        2: _into_split(abs(lat)),
        3: "E" if lon >= 0 else "W",
        4: _into_split(abs(lon)),
    }})

    bio = BytesIO()
    piexif.insert(exif_bytes, image, bio)
    return bio.read()


def tag_plus(image: bytes, plus: str) -> bytes:
    return tag(image, *openlocationcode.decode(plus).latlng())


def untag(image: bytes) -> [float]:
    exif_bytes = piexif.load(image)

    return (
        _merge(*exif_bytes["GPS"][2], exif_bytes["GPS"][1]),
        _merge(*exif_bytes["GPS"][4], exif_bytes["GPS"][3])
    )


def untag_plus(image: bytes) -> str:
    return openlocationcode.encode(*untag(image))
