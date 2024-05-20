def hash(message: str, p: int = 113, m: int = 10 ** 9 + 7) -> int:
    result = 0
    for ascii_l in map(lambda letter: ord(letter), message):
        result = (result + ascii_l * p) % m
    return result