from __future__ import annotations
from .keypair import Keypair
from .utils import modpow


class Client:
    def __init__(self, name: str, keypair: Keypair) -> None:
        self.name = name
        self.keypair: Keypair = keypair
        
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
            ascii_l = modpow(
                base=enc_letter,
                pow=self.keypair.privateLey[0],
                mod=self.keypair.privateLey[1]
            )
            result.append(chr(ascii_l))
        return ''.join(result)
    
    def accept_message(self, name: str, message: list[int]) -> None:
        decrypted_message = self._decrypt(message)
        print('%s: ' % name, decrypted_message)
        
    def send_message(self, user: Client, message: str) -> None:
        encrypted_message = self._encrypt(message, public_key=user.keypair.publicKey)
        user.accept_message(self.name, encrypted_message)