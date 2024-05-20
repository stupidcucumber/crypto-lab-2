import argparse, pathlib, time
import matplotlib.pyplot as plt
from src import Client, RSA, DecryptionType


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', type=int, default=10,
        help='Number of iterations per bitmask length.'
    )
    parser.add_argument(
        '--min-length', type=int, default=3,
        help='Minimal length of a binary representation of the primary number.'
    )
    parser.add_argument(
        '--max-length', type=int, default=20,
        help='Maximal length of a binary representation of the primary number.'
    )
    parser.add_argument(
        '--save', type=pathlib.Path, default=pathlib.Path('performance.png'),
        help='Path to the saved diagram.'
    )
    return parser.parse_args()


def draw_diagram(data: list[tuple[int, float]], save_path: pathlib.Path) -> None:
    length: list[int] = list(map(lambda item: item[0], data))
    duration: list[float] = list(map(lambda item: item[1], data))
    plt.plot(length, duration)
    plt.savefig(save_path)


def single_test(n: int, length: int) -> float:
    bits: str = '0b1' + '0' * (length - 2) + '1'
    start: float = time.perf_counter()
    for _ in range(n):
        rsa = RSA(seed=0, bit_mask=bits)
        alice = Client(
            name='Alice', 
            keypair=rsa.generate_keypair(), 
            decryption_type=DecryptionType.ChineseDecryption,
            logs=False
        )
        bob = Client(
            name='Bob', 
            keypair=rsa.generate_keypair(), 
            decryption_type=DecryptionType.ChineseDecryption,
            logs=False
        )
        
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
    end: float = time.perf_counter()
    return (end - start) / n


if __name__ == '__main__':
    args = parse_arguments()
    data = []
    for length in range(args.min_length, args.max_length):
        try: 
            duration = single_test(n=args.n, length=length)
            data.append(
                (length, duration)
            )
        except Exception as e:
            print('Caught an exception during the excecution: ', e)
    draw_diagram(data=data, save_path=args.save)
    