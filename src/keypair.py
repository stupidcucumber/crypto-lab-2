from pydantic import BaseModel


class Keypair(BaseModel):
    publicKey: tuple[int, int]
    privateKey: tuple[int, int]
    p: int
    q: int