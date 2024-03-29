import base64
from exif import Image
from openlocationcode import openlocationcode
import requests


TOKEN = "ki5w8v4ups9ryg2u"


def _merge(deg: float, min: float, sec: float, ref: str):
    return (1 if ref in "NE" else -1) * (deg + min/60 + sec/3600)


def send(**kwargs):
    global state
    state = requests.post(f"http://[::1]:8001/{TOKEN}/click", json=kwargs).json()


send()

while state["counter"] != 0:
    print(state["counter"], end=' ', flush=True)

    im = Image(base64.b64decode(state["picture"].partition(",")[2]))

    lat = _merge(*im.gps_latitude, im.gps_latitude_ref)
    lon = _merge(*im.gps_longitude, im.gps_longitude_ref)

    send(captcha_response=openlocationcode.encode(lat, lon))


print(state["flag"])
