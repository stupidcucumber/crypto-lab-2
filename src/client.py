from __future__ import annotations
import enum
import math
from .keypair import Keypair
from .utils import modpow


class DecryptionType(enum.IntEnum):
    StandaloneDecryption: int = 0
    ChineeseDecryption: int = 1 


class Client:
    def __init__(self, name: str, keypair: Keypair, decryption_type: DecryptionType) -> None:
        self.name: str = name
        self.keypair: Keypair = keypair
        self.decryption_type: DecryptionType = decryption_type
        
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
        
    def fi(self, n: int) -> int:
        return n - 1
    
    def _standard_decryption(self, symbol: int) -> int:
        return modpow(
                base=symbol,
                pow=self.keypair.privateKey[0],
                mod=self.keypair.privateKey[1]
        )
        
    def _chineese_decryption(self, symbol: int) -> int:
        exponent_1 = self.keypair.privateKey[0] % self.fi(self.keypair.q)
        exponent_2 = self.keypair.privateKey[0] % self.fi(self.keypair.p)
        base_1 = symbol % self.keypair.q
        base_2 = symbol % self.keypair.p
        cong_1 = modpow(base=base_1, pow=exponent_1, mod=self.keypair.q)
        cong_2 = modpow(base=base_2, pow=exponent_2, mod=self.keypair.p)
        m = self._find_d(self.keypair.p, self.keypair.q)
        return (cong_2 + (cong_1 - cong_2) * m * self.keypair.p) % self.keypair.privateKey[1]
        
    def _encrypt(self, message: str, public_key: tuple[int, int]) -> list[int]:
        result = []
        for letter in message:
            ascii_l = ord(letter)
            encrypted_l = modpow(base=ascii_l, pow=public_key[0], mod=public_key[1])
            result.append(encrypted_l)
        return result 
    
    def _decrypt(self, message: list[int]) -> str:
        result = []
        for enc_letter in message:
            if self.decryption_type == DecryptionType.StandaloneDecryption:
                ascii_l = self._standard_decryption(symbol=enc_letter)
            elif self.decryption_type == DecryptionType.ChineeseDecryption:
                ascii_l = self._chineese_decryption(symbol=enc_letter)
            result.append(chr(ascii_l))
        return ''.join(result)
    
    def accept_message(self, name: str, message: list[int]) -> None:
        decrypted_message = self._decrypt(message)
        print('%s: ' % name, decrypted_message)
        
    def send_message(self, user: Client, message: str) -> None:
        encrypted_message = self._encrypt(message, public_key=user.keypair.publicKey)
        user.accept_message(self.name, encrypted_message)