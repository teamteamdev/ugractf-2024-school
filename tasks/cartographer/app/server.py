import base64
import dataclasses
from flask import Flask, render_template, request
import haversine
from kyzylborda_lib.secrets import get_flag, validate_token
from openlocationcode import openlocationcode
import random
from typing import Callable, Tuple

import geotag
from generator import Generator

app = Flask(__name__)


@dataclasses.dataclass
class State:
    token: str
    answer: str = ""
    picture: bytes = bytes()
    counter: int = 2024
    generator: Generator = dataclasses.field(default_factory=Generator)

    def __post_init__(self):
        self.generate_next()

    def generate_next(self, advance: bool = False):
        if advance:
            self.counter -= 1
            self.generator.discard_from_pool(self.answer)

        if self.counter == 0:
            pix, ans = sticker_webp, ""
        else:
            pix, ans = self.generator(self.counter)
            assert check(ans, geotag.untag_plus(pix)), "Yulia is insane"

        self.picture, self.answer = pix, ans

    def into(self) -> dict[str, ...]:
        return {
            "counter": self.counter,
            "picture": "data:image/jpeg;base64," + base64.b64encode(self.picture).decode(),
            "flag": get_flag(self.token) if self.counter == 0 else "s/ugra_[A-Za-z0-9_]+/placeholder/"
        }


# Because defaultdict is not suitable enough.
@dataclasses.dataclass
class NyaaDict(dict):
    gen: Callable  # fn(key) -> value

    def __missing__(self, key):
        self[key] = self.gen(key)
        return self[key]


states = NyaaDict(lambda token: State(token))
with open("sticker.webp", "rb") as f:
    sticker_webp = f.read()


def check(expected: str, value: str) -> bool:
    expected = openlocationcode.decode(expected).latlng()
    value = openlocationcode.decode(value).latlng()
    return haversine.haversine(expected, value, haversine.Unit.METERS) < 100


@app.route("/<token>/")
def index(token: str):
    if not validate_token(token):
        return "Invalid token."
    return render_template("index.html")


@app.route("/<token>/state")
def state(token: str):
    if not validate_token(token):
        return {"error": "Invalid token"}
    return states[token].into()


@app.route("/<token>/click", methods=["POST"])
def click(token: str):
    if not validate_token(token):
        return {"error": "Invalid token"}

    correct = True
    if states[token].counter != 0:
        response = request.json.get("captcha_response")
        correct = type(response) is str and openlocationcode.isFull(response) and check(states[token].answer, response)
        states[token].generate_next(correct)

    return states[token].into() | {"retry_captcha": not correct}
