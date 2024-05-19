from __future__ import annotations
from .keypair import Keypair

class Client:
    def __init__(self, name: str, keypair: Keypair) -> None:
        self.name = name
        self.keypair: Keypair = keypair
        
    def _encrypt(self, message: str) -> list[int]:
        pass
    
    def _decrypt(self, message: list[int]) -> str:
        pass
    
    def accept_message(self, name: str, message: list[int]) -> None:
        decrypted_message = self._decrypt(message)
        print('%s: ' % name, decrypted_message)
        
    def send_message(self, user: Client, message: str) -> None:
        encrypted_message = self._encrypt(message)
        user.accept_message(user.name, encrypted_message)