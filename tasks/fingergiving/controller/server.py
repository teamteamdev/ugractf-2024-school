from kyzylborda_lib.sandbox import start_oneshot
from kyzylborda_lib.secrets import validate_token, get_flag
from kyzylborda_lib.server import telnet

import os


@telnet.listen
async def handle(conn: telnet.Connection):
    token = await conn.with_buffering(conn.get_user())
    if token is None:
        await conn.writeall("Токен не указан. Используйте опцию -l.".encode())
        return
    if not validate_token(token):
        await conn.writeall("Это неверный токен.\n".encode())
        return

    oneshot = await start_oneshot(token, pty=True)
    with oneshot.open("/flag.txt", "w") as f:
        f.write(get_flag(token) + "\n")
    os.chown(oneshot.get_external_file_path("/flag.txt"), 32768, 32768)
    os.chmod(oneshot.get_external_file_path("/flag.txt"), 0o400)
    return oneshot
