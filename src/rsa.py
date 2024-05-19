import math
from .keypair import Keypair
from .utils.generator import PrimeNumberGenerator
from .utils import find_d


class RSA:
    def __init__(self, seed: int = 0, bit_mask: str | None = None) -> None:
        self.seed = seed
        self.generator = iter(
            PrimeNumberGenerator(bit_mask=bit_mask)
        )
        
    def _carmichael_totion(self, num_1: int, num_2: int) -> int:
        return math.lcm(num_1, num_2)
    
    def generate_keypair(self, e: int = 23) -> Keypair:
        d = 1
        while d == 1:
            p = next(self.generator)
            q = next(self.generator)
            n = q * p
            carmichael_lambda = self._carmichael_totion(p - 1, q - 1)
            d = find_d(e=e, m=carmichael_lambda)
        return Keypair(
            privateKey=(d, n),
            publicKey=(e, n),
            p=p,
            q=q
        )
