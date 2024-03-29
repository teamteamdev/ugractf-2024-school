import os
from epkp import client

c = client.Client("server", 17427)

c.establish_connection(os.urandom(31))
c.send_encrypted(b"""Hi Alice! Hope nobody eavesdrops on our conversation. Any progress? Send news and I'll try to help.""")

c.recv_encrypted()

c.send_encrypted(f"Try this one: {os.environ['FLAG']}".encode())

c.sock.close()
