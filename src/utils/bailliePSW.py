from typing import Iterator
from .millerrabin import miller_rabin_test, find_k_m


def _sequence() -> Iterator[int]:
    start = 5
    step = 0
    while True:
        yield start * ((-1) ** step)
        start += 2
        step += 1
        
        
def _lukas_number_in_sequence(index: int, init_0: int, init_1: int, P: int, Q: int) -> int:
    if index < 2:
        return index
    current_step = 1
    buffer = [init_0, init_1]
    while current_step != index:
        current_step += 1
        next_U = P * buffer[1] - Q * buffer[0]
        buffer[0] = buffer[1]
        buffer[1] = next_U
    return buffer[-1]


def _jacobi(a: int, n: int) -> int:
    if n <= 0 or not n & 1:
        raise ValueError('n must be greater than zero and must be an odd.')
    a = a % n
    t = 1
    r = 0
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        r = n
        n = a
        a = r
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    if n == 1:
        return t
    return 0


def _strong_lukas_test(number: int, D: int) -> bool:
    P = 1
    Q = (1 - D) / 4
    s, d = find_k_m(number - 1)
    first_part = (_lukas_number_in_sequence(index=d, init_0=0, init_1=1, P=P, Q=Q) % number == 0)
    if first_part:
        return True
    for r in range(0, s):
        v_index = 2 ** r * d
        if (_lukas_number_in_sequence(index=v_index, init_0=2, init_1=P, P=P, Q=Q) % number) == 0:
            return True
    return False


def baillie_psw_test(number: int) -> bool:
    if number == 1:
        return False
    if number in [2, 3, 5]:
        return True
    if not number & 1:
        return False
    if not miller_rabin_test(number=number):
        return False

    for element in _sequence():
        jacobi_symbol = _jacobi(element, number)
        if jacobi_symbol == -1:
            D = element
            break
    lukas_pseudonumber = _strong_lukas_test(number=number, D=D)
    return not lukas_pseudonumber