import collections.abc
import functools
import itertools
import typing

import aoc2025


def has_double_digits(value: str) -> bool:
    if (digits := len(value)) % 2 == 0:
        return value[: digits // 2] == value[digits // 2 :]
    else:
        return False


@functools.cache
def get_prime_factors(number: int) -> set[int]:
    return {divisor for divisor in range(1, number // 2 + 1) if number % divisor == 0}


def has_repeated_digits(value: str) -> bool:
    for length in get_prime_factors(len(value)):
        if len(set(itertools.batched(value, n=length))) == 1:
            return True
    else:
        return False


def iter_invalid_ids(
    path_to_input: str, is_invalid: typing.Callable[[str], bool]
) -> collections.abc.Iterator[int]:
    with open(file=path_to_input) as f:
        for upper_lower in f.read().split(","):
            lower, upper = map(int, upper_lower.split("-"))
            yield from map(int, filter(is_invalid, map(str, range(lower, upper + 1))))


@aoc2025.expects(18595663903)
def part_one(path_to_input: str) -> int:
    return sum(
        iter_invalid_ids(is_invalid=has_double_digits, path_to_input=path_to_input)
    )


@aoc2025.expects(19058204438)
def part_two(path_to_input: str) -> int:
    return sum(
        iter_invalid_ids(is_invalid=has_repeated_digits, path_to_input=path_to_input)
    )
