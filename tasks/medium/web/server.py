from flask import abort, Flask, redirect, render_template, request, url_for
import json
from kyzylborda_lib.secrets import get_secret, validate_token
import os
import secrets
import sqlite3


app = Flask(__name__)
con = sqlite3.connect("/state/medium.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS article(token, id, title, content, edit_password, view_full_password)")


@app.route("/<token>/")
def list_articles(token: str):
    if not validate_token(token):
        return "Invalid token."

    res = cur.execute("SELECT id, title FROM article WHERE token = ?", (token,))
    rows = res.fetchall()

    articles = [{"id": row[0], "title": row[1]} for row in rows[::-1]]

    return render_template("list.html", articles=articles)


@app.route("/<token>/<id>/")
def article(token: str, id: str):
    if not validate_token(token):
        return "Invalid token."

    if "password" in request.args:
        response = redirect(url_for("article", token=token, id=id), code=303)
        response.set_cookie("password", request.args["password"], path=f"/{token}/{id}", max_age=2147483647)
        return response
    else:
        return render_template("article.html")


@app.route("/<token>/<id>/retrieve", methods=["POST"])
def retrieve(token: str, id: str):
    if not validate_token(token):
        return "Invalid token."

    if not isinstance(request.json, dict):
        abort(400)
    if "password" not in request.json:
        abort(400)
    password = request.json["password"]

    res = cur.execute("SELECT title, content, edit_password, view_full_password FROM article WHERE token = ? AND id = ?", (token, id))
    row = res.fetchone()
    if row is None:
        return {
            "title": "Кто здесь?",
            "content": {
                "blocks": [
                    {
                        "id": "empty",
                        "type": "paragraph",
                        "data": {
                            "text": "Такой страницы нет. Хотите, чтобы была &mdash; <a href=\"new\">напишите статью сами</a>.",
                        },
                    },
                ],
                "time": 0,
                "version": "2.29.1",
            }
        }

    title, content, edit_password, view_full_password = row
    content = json.loads(content)

    if isinstance(content, dict) and isinstance(content.get("blocks"), list):
        if password == edit_password:
            pass
        elif password == view_full_password:
            content["blocks"] = [
                block for block in content["blocks"]
                if not isinstance(block, dict) or block.get("type") != "paid"
            ]
        else:
            i = 0
            while i < len(content["blocks"]) and (not isinstance(content["blocks"][i], dict) or content["blocks"][i].get("type") != "paid"):
                i += 1
            content["blocks"] = content["blocks"][:i + 1]

    return {
        "title": title,
        "content": content,
        "view_full_password": view_full_password if password == edit_password else None,
    }


@app.route("/<token>/<id>/update", methods=["POST"])
def update(token: str, id: str):
    if not validate_token(token):
        return "Invalid token."

    if not isinstance(request.json, dict):
        abort(400)
    if "title" not in request.json or "content" not in request.json or "password" not in request.json:
        abort(400)
    title = request.json["title"]
    content = request.json["content"]
    password = request.json["password"]

    res = cur.execute("SELECT edit_password FROM article WHERE token = ? AND id = ?", (token, id))
    row = res.fetchone()
    if row is None:
        abort(404)
    edit_password, = row

    if password != edit_password:
        abort(403)

    content = json.dumps(content)
    cur.execute("UPDATE article SET title = ?, content = ? WHERE token = ? AND id = ?", (title, content, token, id))
    con.commit()

    reload(token, id)

    return "", 204


@app.route("/<token>/new", methods=["GET"])
def new(token: str):
    if not validate_token(token):
        return "Invalid token."

    if "activate" in request.args:
        id = get_secret("writeup_id", token)
        edit_password = secrets.token_urlsafe(16)
        view_full_password = get_secret("admin_password", token)

        cur.execute(
            "DELETE FROM article WHERE token = ? AND id = ?",
            (token, id),
        )
        con.commit()
    else:
        id = secrets.token_urlsafe(16)
        edit_password = secrets.token_urlsafe(16)
        view_full_password = secrets.token_urlsafe(16)

    cur.execute(
        "INSERT INTO article(token, id, title, content, edit_password, view_full_password) VALUES (?, ?, ?, ?, ?, ?)",
        (token, id, "", json.dumps({"blocks": [], "time": 0, "version": "2.29.1"}), edit_password, view_full_password),
    )
    con.commit()

    reload(token, id)

    response = redirect(url_for("article", token=token, id=id), code=303)
    response.set_cookie("password", edit_password, path=f"/{token}/{id}", max_age=2147483647)
    return response


def reload(token: str, id: str):
    os.makedirs("/state/markers", exist_ok=True)
    with open(os.path.join(f"/state/markers/{token}"), "w") as f:
        f.write(id)
