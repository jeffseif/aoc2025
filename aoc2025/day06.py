import collections.abc
import functools
import itertools
import operator

import aoc2025


OPERAND_TO_FUNC = {
    "+": operator.add,
    "*": operator.mul,
}


def iter_solution(
    path_to_input: str, is_simple_pivot: bool
) -> collections.abc.Iterator[int]:
    with open(file=path_to_input) as f:
        number_rows = [line.strip("\n") for line in f]
    operand_row = number_rows.pop()

    number_lists: collections.abc.Iterable[collections.abc.Iterable[str]]
    if is_simple_pivot:
        number_lists = zip(*map(str.split, number_rows), strict=True)
    else:
        idxs = [idx for idx, char in enumerate(operand_row) if char != " "]
        idxs.append(len(operand_row) + 1)
        number_lists = (
            map("".join, zip(*tuple(row[left : right - 1] for row in number_rows)))
            for left, right in itertools.pairwise(idxs)
        )
    for operand, number_list in zip(operand_row.split(), number_lists, strict=True):
        yield functools.reduce(OPERAND_TO_FUNC[operand], map(int, number_list))


@aoc2025.expects(4412382293768)
def part_one(path_to_input: str) -> int:
    return sum(iter_solution(path_to_input=path_to_input, is_simple_pivot=True))


@aoc2025.expects(7858808482092)
def part_two(path_to_input: str) -> int:
    return sum(iter_solution(path_to_input=path_to_input, is_simple_pivot=False))
