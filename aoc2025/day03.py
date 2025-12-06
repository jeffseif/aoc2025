import collections.abc
import functools

import aoc2025


def iter_bank(path_to_input: str) -> collections.abc.Iterator[str]:
    with open(file=path_to_input) as f:
        yield from map(str.strip, f)


def get_max_n_joltage_for_bank(bank: str, number_of_digits: int) -> int:
    digits = []
    left, right = 0, len(bank) - number_of_digits + 1
    for _ in range(number_of_digits):
        maximum = max(bank[left:right])
        idx = left + bank[left:right].index(maximum)
        digits.append(maximum)
        left, right = idx + 1, right + 1
    return sum(
        digit * 10 ** (number_of_digits - power - 1)
        for power, digit in enumerate(map(int, digits))
    )


@aoc2025.expects(17524)
def part_one(path_to_input: str) -> int:
    return sum(
        map(
            functools.partial(get_max_n_joltage_for_bank, number_of_digits=2),
            iter_bank(path_to_input=path_to_input),
        )
    )


@aoc2025.expects(173848577117276)
def part_two(path_to_input: str) -> int:
    return sum(
        map(
            functools.partial(get_max_n_joltage_for_bank, number_of_digits=12),
            iter_bank(path_to_input=path_to_input),
        )
    )
