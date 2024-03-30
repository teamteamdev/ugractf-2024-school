#!/usr/bin/env python3

from kyzylborda_lib.secrets import get_flag, validate_token

import aiohttp.web
from jinja2 import FileSystemLoader
import aiohttp_jinja2 as jinja2
import json
import os
import random
import sys
import PIL.Image


BASE_DIR = os.path.dirname(__file__)

font_img = PIL.Image.open("font.png")
font_letters = "acegkmnopruxy_"
font_pos = 0
FONT = {}
for x in range(1, font_img.width):
    prev, cur = font_img.getpixel((x - 1, 0))[1], font_img.getpixel((x, 0))[1]
    if (prev, cur) == (0, 255):
        Y = 0
        for y in range(2, font_img.height):
            if font_img.getpixel((font_pos, y)) == (255, 0, 255, 255):
                Y = y
                break

        FONT[font_letters[0]] = font_img.crop((font_pos, 1, x, Y))
        font_letters = font_letters[1:]
    elif (prev, cur) == (255, 0):
        font_pos = x


def make_app(state_dir):
    app = aiohttp.web.Application()
    routes = aiohttp.web.RouteTableDef()
    routes.static("/static", os.path.join(BASE_DIR, "static"))


    @routes.get("/{token}")
    @routes.get("/{token}/")
    async def root(request):
        return aiohttp.web.HTTPMovedPermanently(f"/{request.match_info['token']}/0")


    @routes.get("/{token}/{level:\d+}")
    async def main(request):
        if not validate_token(token := request.match_info["token"]):
            raise aiohttp.web.HTTPForbidden

        flag = get_flag(token)

        if not 0 <= (level := int(request.match_info["level"])) <= len(flag):
            raise aiohttp.web.HTTPBadRequest

        return jinja2.render_template("main.html", request, {"level": level, "levels": len(flag)})


    @routes.get("/{token}/{level:\d+}/ws")
    async def websocket_handler(request):
        if not validate_token(token := request.match_info["token"]):
            raise aiohttp.web.HTTPForbidden

        flag = get_flag(token)

        if not 0 <= (level := int(request.match_info["level"])) <= len(flag):
            raise aiohttp.web.HTTPBadRequest


        ws = aiohttp.web.WebSocketResponse(heartbeat=5, receive_timeout=15, timeout=15, max_msg_size=2048)
        await ws.prepare(request)

        game_x = 14
        game_y = 14
        game_z = 10

        real_field = [[[0 for x in range(game_x)] for y in range(game_y)] for z in range(game_z)]
        for _x in range(game_x):
            for _y in range(game_y):
                for _z in range(game_z):
                    real_field[_z][_y][_x] = int(random.random() < (0.133 + 0.7 * (level / len(flag))))

        if level > 0:
            letter = flag[level - 1]
            letter_img = FONT[letter].copy()
            l_width, l_height = letter_img.width, letter_img.height

            disallow_2 = (l_height > game_z)
            orientation = random.randint(0 if level < 38 else 1, 1 if disallow_2 else 2)
            if level <= 13:
                orientation = 0

            if orientation == 0:
                px = random.randint(0, game_x - l_width)
                py = random.randint(0, game_y - l_height)
                pz = random.randint(0, game_z - 1)
            elif orientation == 1:
                px = random.randint(0, game_x - 1)
                py = random.randint(0, game_y - l_height)
                pz = random.randint(0, game_z - l_width)
                letter_img = letter_img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            elif orientation == 2:
                px = random.randint(0, game_x - l_width)
                py = random.randint(0, game_y - 1)
                pz = random.randint(0, game_z - l_height)

            points = []
            for lx in range(l_width):
                for ly in range(l_height):
                    if letter_img.getpixel((lx, ly)) == (0, 0, 0, 255):
                        if orientation == 0:
                            points.append((px + lx, py + ly, pz))
                        elif orientation == 1:
                            points.append((px, py + ly, pz + lx))
                        elif orientation == 2:
                            points.append((px + lx, py, pz + ly))

            for opx, opy, opz in points:
                for dx in [-3, -2, -1, 0, 1, 2, 3]:
                    for dy in [-3, -2, -1, 0, 1, 2, 3]:
                        for dz in [-3, -2, -1, 0, 1, 2, 3]:
                            if 0 <= opx + dx < game_x:
                                if 0 <= opy + dy < game_y:
                                    if 0 <= opz + dz < game_z:
                                        real_field[opz + dz][opy + dy][opx + dx] = 0

            for opx, opy, opz in points:
                real_field[opz][opy][opx] = 1


        field = [[[None for x in range(game_x)] for y in range(game_y)] for z in range(game_z)]

        await ws.send_json({"start": True, "z": game_z, "y": game_y, "x": game_x})
        if os.environ.get("DEBUG_VISUALIZATION") or request.cookies.get("debug-visualization-fe833601"):
            for _x in range(game_x):
                for _y in range(game_y):
                    for _z in range(game_z):
                        if real_field[_z][_y][_x]:
                            await ws.send_json({"update": [{"x": _x, "y": _y, "z": _z, "state": "bomb"}]})

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                except:
                    await ws.send_json({"error": "Hekopp. JSON"})
                    return ws

                try:
                    event = data["event"]
                    x = data["x"]
                    y = data["y"]
                    z = data["z"]
                    assert 0 <= x < game_x
                    assert 0 <= y < game_y
                    assert 0 <= z < game_z
                except:
                    await ws.send_json({"error": "Hekopp. cogep. event, x, y, z"})
                    return ws
                
                if event == "click":
                    if field[z][y][x] is True:  # flag
                        pass
                    elif real_field[z][y][x] == 1:  # bomb
                        await ws.send_json({"update": [{"x": x, "y": y, "z": z, "state": "bomb"}]})
                        await ws.send_json({"error": "Hy makoe :("})
                        return ws
                    else:
                        c = 0
                        for _x in range(x - 1, x + 2):
                            for _y in range(y - 1, y + 2):
                                for _z in range(z - 1, z + 2):
                                    if _x in range(game_x) and _y in range(game_y) and _z in range(game_z):
                                        c += real_field[_z][_y][_x]
                        field[z][y][x] = c
                        await ws.send_json({"update": [{"x": x, "y": y, "z": z, "state": "open", "count": c}]})

                        win = True
                        for _x in range(game_x):
                            for _y in range(game_y):
                                for _z in range(game_z):
                                    # if an unopened field is present
                                    if (field[_z][_y][_x] is None or field[_z][_y][_x] is True) and real_field[_z][_y][_x] == 0:
                                        win = False
                                        break
                        if win:
                            await ws.send_json({"win": True})
                            return ws
                elif event == "flag":
                    if field[z][y][x] is None:
                        field[z][y][x] = True
                        await ws.send_json({"update": [{"x": x, "y": y, "z": z, "state": "flag"}]})
                    elif field[z][y][x] is True:
                        field[z][y][x] = None
                        await ws.send_json({"update": [{"x": x, "y": y, "z": z, "state": "noflag"}]})
            elif msg.type == aiohttp.WSMsgType.ERROR:
                return ws


    app.add_routes(routes)
    jinja2.setup(app, loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])

    if os.environ.get("DEBUG") == "F":
        aiohttp.web.run_app(app, host="0.0.0.0", port=31737)
    else:
        aiohttp.web.run_app(app, path=os.path.join(sys.argv[1], "canep.sock"))

