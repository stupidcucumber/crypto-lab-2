from .keypair import Keypair


class RSA:
    def __init__(self, seed: int = 0) -> None:
        self.seed = seed
    
    def generate_keypair(self) -> Keypair:
        pass