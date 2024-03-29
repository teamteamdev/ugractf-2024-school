from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


class ECDH:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP521R1())
        self.public_key = self.private_key.public_key()

    def get_public_key(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=Encoding.X962,
            format=PublicFormat.UncompressedPoint
        )

    def get_shared_key(self, peer_public_bytes: bytes) -> bytes:
        peer_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP521R1(), peer_public_bytes
        )
        return self.private_key.exchange(ec.ECDH(), peer_public_key)
