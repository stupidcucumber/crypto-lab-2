import argparse
from src import Client, RSA, DecryptionType


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bits', type=str, default='0b000001',
        help='Mask of the required bits in the prime number.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    rsa = RSA(seed=0, bit_mask=args.bits)
    alice = Client(
        name='Alice', 
        keypair=rsa.generate_keypair(), 
        decryption_type=DecryptionType.ChineseDecryption
    )
    bob = Client(
        name='Bob', 
        keypair=rsa.generate_keypair(), 
        decryption_type=DecryptionType.ChineseDecryption
    )
    print('Alice\'s keypair: ', alice.keypair)
    print('Bob\'s keypair: ', bob.keypair)
    
    alice.send_message(
        user=bob,
        message='Hi Bob! How are you?'
    )
    bob.send_message(
        user=alice,
        message='I am fine, what about you?'
    )
    alice.send_message(
        user=bob,
        message='I am testing my implementation of the RSA algorithm!'
    )
    bob.send_message(
        user=alice,
        message='Cool.'
    )
    