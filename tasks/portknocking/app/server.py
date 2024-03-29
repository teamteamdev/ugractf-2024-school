import socketserver

from epkp.ecdhe import ECDH
from epkp.matrix import Encryptor
from epkp.client import recvexactly


class Handler(socketserver.BaseRequestHandler):
    def send_encrypted(self, data: bytes):
        encrypted = self.encryptor.encrypt(data)
        self.request.sendall((len(encrypted) // 16).to_bytes(2, "little"))
        self.request.sendall(encrypted)

    def recv_encrypted(self) -> bytes:
        size = int.from_bytes(recvexactly(self.request, 2), "little") * 16
        return self.encryptor.decrypt(recvexactly(self.request, size))

    def handle(self):
        try:
            assert recvexactly(self.request, 5) == b'EPKP\xfa', "Invalid client tag"

            size = recvexactly(self.request, 1)[0]
            peer_public = recvexactly(self.request, size)

            e = ECDH()

            our_public = e.get_public_key()

            self.request.sendall(b'EPKP\xfb' + bytearray([len(our_public)]) + our_public)

            shared = e.get_shared_key(peer_public)[:32]
            assert len(shared) == 32, "Invalid shared key"

            self.encryptor = Encryptor(shared)

            assert self.recv_encrypted() == b"Knock-knock!", "Invalid client ID pre-request"
            self.send_encrypted(b"Who's there?")
            
            assert len(self.recv_encrypted()) == 31, "Client ID is invalid"
            self.send_encrypted(b"\x01")

            self.recv_encrypted()
            self.send_encrypted(b"Hi! Found the safe box, but it's locked. Got the key?")
            self.recv_encrypted()
        finally:
            self.request.close()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", 17427), Handler) as server:
    server.serve_forever()
