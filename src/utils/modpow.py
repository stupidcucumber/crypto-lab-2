import functools


def modpow(base: int, pow: int, mod: int) -> int:
    binary_power: str = bin(pow).split('b', maxsplit=1)[1]
    previous_mod: int = base % mod
    mods_array: list = [previous_mod] if binary_power[-1] == '1' else []
    for value in binary_power[::-1][1:]:
        previous_mod = (previous_mod ** 2) % mod
        if value == '1':
            mods_array.append(previous_mod)
    return functools.reduce(lambda x, y: x * y, mods_array) % mod
    