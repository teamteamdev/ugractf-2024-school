#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token

import aiohttp.web
import aiohttp_jinja2 as jinja2
import hashlib
import os
import random
import sys
from jinja2 import FileSystemLoader


BASE_DIR = os.path.dirname(__file__)


def make_app(state_dir):
    app = aiohttp.web.Application()
    routes = aiohttp.web.RouteTableDef()
    routes.static("/static", os.path.join(BASE_DIR, "static"))


    @routes.get("/{token}")
    async def slashless(request):
        return aiohttp.web.HTTPMovedPermanently(f"/{request.match_info['token']}/")


    @routes.get("/{token}/")
    @routes.post("/{token}/")
    async def main(request):
        if not validate_token(token := request.match_info["token"]):
            raise aiohttp.web.HTTPForbidden

        cookie_name = hashlib.sha1(f"234234{token}fgsfdsgsdf".encode()).hexdigest()

        if request.method == "POST":
            errors = {}
            
            data = await request.post()
            if "challenge1" in data and data["challenge1"] != "fourth":
                errors["challenge1"] = True
            if "challenge2" in data and data["challenge2"] != "iwbnfouevcmisieh wvudbqvgovernment":
                errors["challenge2"] = True

            if not errors:
                response = aiohttp.web.HTTPFound(".")
                response.set_cookie(cookie_name, "1")
                return response
            else:
                return jinja2.render_template("main.html", request, {"errors": errors})

        if request.cookies.get(cookie_name):
            numbers = list(range(len(flag := get_flag(token))))
            random.shuffle(numbers)
            numbers = numbers[:len(numbers) // 2]
            return jinja2.render_template("main.html", request, {"flag": flag, "numbers": numbers})
        else:
            return jinja2.render_template("main.html", request, {})


    @routes.get("/{token}/click")
    async def main(request):
        if not validate_token(token := request.match_info["token"]):
            raise aiohttp.web.HTTPForbidden
   
        dirname = f"{state_dir}/{token}"
        os.makedirs(dirname, exist_ok=True)
        open(f"{dirname}/clicks.txt", "a").write(request.query.get("value", "") + "\n")
        
        return aiohttp.web.json_response(True)


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])

    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(app, host="0.0.0.0", port=31377)
    else:
        aiohttp.web.run_app(app, path=os.path.join(sys.argv[1], "snapandgo.sock"))
