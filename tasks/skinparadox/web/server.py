from flask import Flask, render_template, request
from kyzylborda_lib.secrets import get_flag, validate_token


def generate_purplesyringa_key(token):
    arr = [ord(c) for c in token]
    for x in range(999, 0, -1):
        i = (x * 743893 >> 16) % 16
        j = (x * 433 >> 4) % 16
        if i != j:
            arr[i] = (arr[i] - arr[j]) % 256
    for i in range(16):
        arr[i] = arr[i] or 256
    for i in range(15, 0, -1):
        arr[i] = arr[i] * pow(arr[i - 1], -1, 257) % 257
    for i in range(16):
        arr[i] = arr[i] % 256
    return arr


def generate_ucucuga_key(token, purplesyringa_key):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
    for c in purplesyringa_key:
        i = c % len(token)
        tmp = token[i:] + token[:i]
        token = ""
        for i in range(len(tmp)):
            token += ALPHABET[(sum(map(ord, tmp[:i + 1])) + i) % len(ALPHABET)]
    return token



app = Flask(__name__)

@app.route("/<token>/")
def index(token: str):
    if not validate_token(token):
        return "Invalid token."
    return render_template("index.html")

@app.route("/<token>/get-flag/<ucucuga_key>")
def get_flag_page(token: str, ucucuga_key: str):
    if not validate_token(token):
        return "Invalid token."
    purplesyringa_key = generate_purplesyringa_key(token)
    if ucucuga_key != generate_ucucuga_key(token, purplesyringa_key):
        return "Invalid key."
    return get_flag(token)
