from __future__ import annotations
import enum
from .keypair import Keypair
from .utils import modpow, find_d, hash


class DecryptionType(enum.IntEnum):
    StandaloneDecryption: int = 0
    ChineseDecryption: int = 1 


class Client:
    def __init__(self, name: str, keypair: Keypair, decryption_type: DecryptionType,
                 logs: bool = True) -> None:
        self.name: str = name
        self.keypair: Keypair = keypair
        self.decryption_type: DecryptionType = decryption_type
        self.logs: bool = logs
        
    def fi(self, n: int) -> int:
        return n - 1
    
    def _standard_decryption(self, symbol: int, key: tuple[int, int]) -> int:
        return modpow(
                base=symbol,
                pow=key[0],
                mod=key[1]
        )
        
    def _chineese_decryption(self, symbol: int, key: tuple[int, int]) -> int:
        exponent_1 = key[0] % self.fi(self.keypair.q)
        exponent_2 = key[0] % self.fi(self.keypair.p)
        base_1 = symbol % self.keypair.q
        base_2 = symbol % self.keypair.p
        cong_1 = modpow(base=base_1, pow=exponent_1, mod=self.keypair.q)
        cong_2 = modpow(base=base_2, pow=exponent_2, mod=self.keypair.p)
        m = find_d(self.keypair.p, self.keypair.q)
        return (cong_2 + (cong_1 - cong_2) * m * self.keypair.p) % key[1]
        
    def _encrypt(self, message: str, key: tuple[int, int]) -> list[int]:
        result = []
        for letter in message:
            ascii_l = ord(letter)
            encrypted_l = modpow(base=ascii_l, pow=key[0], mod=key[1])
            result.append(encrypted_l)
        return result 
    
    def _decrypt(self, message: list[int], key: tuple[int, int], decryption_type: DecryptionType) -> str:
        result = []
        for enc_letter in message:
            if decryption_type == DecryptionType.StandaloneDecryption:
                ascii_l = self._standard_decryption(symbol=enc_letter, key=key)
            elif decryption_type == DecryptionType.ChineseDecryption:
                ascii_l = self._chineese_decryption(symbol=enc_letter, key=key)
            result.append(chr(ascii_l))
        return ''.join(result)
    
    def _sign(self, message: str) -> list[int]:
        m_hash = hex(hash(message=message)).split('x')[-1]
        signature = self._encrypt(message=m_hash, key=self.keypair.privateKey)
        return signature
    
    def accept_message(self, name: str, message: list[int], signature: list[int], sender_public_key: tuple[int, int]) -> None:
        decrypted_message = self._decrypt(message, key=self.keypair.privateKey, decryption_type=self.decryption_type)
        m_hash = hex(hash(message=decrypted_message))
        m_hash_decrypted = self._decrypt(signature, key=sender_public_key, decryption_type=DecryptionType.StandaloneDecryption)
        if self.logs:
            print('%s: ' % name, decrypted_message, '(got hash: 0x%s, actual hash: %s)' % (m_hash_decrypted, m_hash))
        
    def send_message(self, user: Client, message: str) -> None:
        encrypted_message = self._encrypt(message, key=user.keypair.publicKey)
        signature = self._sign(message=message)
        user.accept_message(self.name, encrypted_message, signature, sender_public_key=self.keypair.publicKey)