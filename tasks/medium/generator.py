import json
from kyzylborda_lib.secrets import get_flag, get_secret, get_token
import requests


def generate():
    token = get_token()
    flag = get_flag()

    with open("writeup.json") as f:
        writeup = json.loads(f.read().replace("{{flag}}", flag))

    session = requests.Session()
    url = session.get(f"https://medium.s.2024.ugractf.ru/{token}/new?activate=1").url
    password = session.cookies.get_dict()["password"]
    if session.post(f"{url}update", json={"password": password, **writeup}).status_code != 204:
        raise RuntimeError("Oops, failed to generate")
