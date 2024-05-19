import random
from .modpow import modpow


def find_k_m(number: int) -> tuple[int, int]:
    k: int = 0
    power: int = 1
    m: int = number
    while (number / power).is_integer():
        m = int(number / power)
        power *= 2
        k += 1
    return k-1, m


def _miller_rabin_single_step(number: int, q: int, k: int, a: int) -> bool:
    b = modpow(base=a, pow=q, mod=number)
    prime_test = -1 % number
    if b == 1 or b == prime_test:
        return True
    for _ in range(0, k):
        b = modpow(b, 2, mod=number)
        if b % number == prime_test:
            return True
    return False


def miller_rabin_test(number: int, tests: int = 5) -> bool:
    if number in [2, 3, 5]:
        return True
    if not number & 1:
        return False
    temp: int = number - 1
    k, q = find_k_m(number=temp)
    for _ in range(tests):
        a = random.randint(2, number-1)
        result = _miller_rabin_single_step(number=number, q=q, k=k, a=a)
        if not result:
            return False
    return True
