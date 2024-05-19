import itertools
from typing import Iterator
from .bailliePSW import baillie_psw_test


class PrimeNumberGenerator:
    def __init__(self, bit_mask: str | None = None) -> None:
        self.bit_mask = bit_mask
        
    def _gather_new_number(self, number: str, new_values: list[int], indeces: list[int]) -> str:
        reverse = list(number[::-1])
        for index, value in zip(indeces, new_values): 
            reverse[index] = str(value)
        return int(''.join(reverse[::-1]), base=2) 
        
    def _next_number(self) -> Iterator[int]:
        if self.bit_mask is not None:
            number: str = self.bit_mask
            zero_indeces = [
                index for index, value in enumerate(number.split('b')[-1][::-1]) if value == '0' 
            ]
            for combination in itertools.product(*([[0, 1]] * len(zero_indeces))):
                yield self._gather_new_number(number=number, new_values=combination, indeces=zero_indeces)
        else:
            for count in itertools.count():
                yield count + 1
    
    def __iter__(self) -> Iterator[int]:
        for number in self._next_number():
            if baillie_psw_test(number=number):
                yield number