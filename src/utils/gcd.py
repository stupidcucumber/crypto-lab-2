import math


def find_d(e: int, m: int) -> int:
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