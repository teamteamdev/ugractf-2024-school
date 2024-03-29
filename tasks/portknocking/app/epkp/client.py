import socket

from .ecdhe import ECDH
from .matrix import Encryptor


def recvexactly(sock: socket.socket, n: int) -> bytes:
    buffer = b""
    remaining = n
    while remaining > 0:
        data = sock.recv(min(remaining, 1024))
        if not data:
            raise EOFError("Connection closed")
        buffer += data
        remaining -= len(data)
    return buffer


class Client:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port), 2)

    def send_encrypted(self, data: bytes):
        encrypted = self.encryptor.encrypt(data)
        self.sock.sendall((len(encrypted) // 16).to_bytes(2, "little"))
        self.sock.sendall(encrypted)

    def recv_encrypted(self) -> bytes:
        size = int.from_bytes(recvexactly(self.sock, 2), "little") * 16
        return self.encryptor.decrypt(recvexactly(self.sock, size))

    def establish_connection(self, client_id: bytes):
        assert len(client_id) == 31, "Invalid client ID"

        e = ECDH()

        our_public = e.get_public_key()

        self.sock.sendall(b'EPKP\xfa' + bytearray([len(our_public)]) + our_public)

        assert recvexactly(self.sock, 5) == b'EPKP\xfb', "Invalid server tag"

        size = recvexactly(self.sock, 1)[0]
        peer_public = recvexactly(self.sock, size)

        shared = e.get_shared_key(peer_public)[:32]
        assert len(shared) == 32, "Invalid shared key"

        self.encryptor = Encryptor(shared)

        self.send_encrypted(b"Knock-knock!")
        assert self.recv_encrypted() == b"Who's there?", "Invalid server ID request"

        self.send_encrypted(client_id)
        assert self.recv_encrypted() == b"\x01", "Client is already connected"
