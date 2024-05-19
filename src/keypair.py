from pydantic import BaseModel


class Keypair(BaseModel):
    publicKey: tuple[int, int]
    privateLey: tuple[int, int]