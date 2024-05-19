import math
from .keypair import Keypair
from .utils.generator import PrimeNumberGenerator


class RSA:
    def __init__(self, seed: int = 0, bit_mask: str | None = None) -> None:
        self.seed = seed
        self.generator = iter(
            PrimeNumberGenerator(bit_mask=bit_mask)
        )
        
    def _carmichael_totion(self, num_1: int, num_2: int) -> int:
        return math.lcm(num_1, num_2)
    
    def _find_d(self, e: int, m: int) -> int:
        a = e
        b = m
        x = 0
        y = 1
        while True:
            if a == 1:
                return y
            if a == 0:
                raise ValueError('Does not exists!')
            q = math.floor(b / a)
            b = b - a * q
            x = x + q * y
            if b == 1:
                return m - x
            if b == 1:
                raise ValueError('Does not exists!')
            q = math.floor(a / b)
            a = a - b * q
            y = y + q * x
    
    def generate_keypair(self, e: int = 23) -> Keypair:
        p = next(self.generator)
        q = next(self.generator)
        n = q * p
        carmichael_lambda = self._carmichael_totion(p - 1, q - 1)
        d = self._find_d(e=e, m=carmichael_lambda)
        return Keypair(
            privateLey=(d, n),
            publicKey=(e, n)
        )
