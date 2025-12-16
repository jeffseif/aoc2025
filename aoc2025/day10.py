import collections
import collections.abc
import dataclasses
import functools
import itertools
import operator
import re

import aoc2025


def xor_reduce(it: collections.abc.Iterable[int]) -> int:
    return functools.reduce(operator.xor, it, initial=0)


@functools.cache
def iter_presses(buttons: tuple[int, ...], goal: int) -> list[tuple[int, ...]]:
    def it() -> collections.abc.Iterator[tuple[int, ...]]:
        for count in range(0, len(buttons) + 1):
            for presses in itertools.combinations(buttons, r=count):
                if xor_reduce(presses) == goal:
                    yield presses

    return list(it())


@functools.cache
def iter_multipresses(
    buttons: tuple[int, ...], joltages: tuple[int, ...]
) -> list[tuple[int, ...]]:
    def it() -> collections.abc.Iterator[tuple[int, ...]]:
        goal = sum((value & 1) << bit for bit, value in enumerate(joltages))
        for odd_presses in iter_presses(buttons=buttons, goal=goal):
            covered = collections.Counter(
                bit
                for press in odd_presses
                for bit in range(len(joltages))
                if press & (1 << bit)
            )
            remaining = tuple(
                (count - covered.get(bit, 0)) // 2 for bit, count in enumerate(joltages)
            )

            if any(_ < 0 for _ in remaining):
                continue
            elif any(remaining):
                for even_presses in iter_multipresses(
                    buttons=buttons, joltages=remaining
                ):
                    yield odd_presses + even_presses + even_presses
            else:
                yield odd_presses

    return list(it())


@dataclasses.dataclass(frozen=True)
class Machine:
    buttons: tuple[int, ...]
    goal: int
    joltages: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> Machine:
        return cls(
            buttons=tuple(
                sum(1 << bit for bit in map(int, button.group().split(",")))
                for button in re.finditer(pattern=r"(?<=\()[0-9,]+", string=line)
            ),
            goal=sum(
                on_or_off << bit
                for bit, on_or_off in enumerate(
                    char == "#"
                    for match in re.finditer(pattern="[.#]+", string=line)
                    for char in match.group()
                )
            ),
            joltages=tuple(
                map(
                    int,
                    (
                        number
                        for match in re.finditer("(?<={)[0-9,]+", string=line)
                        for number in match.group().split(",")
                    ),
                )
            ),
        )


def iter_machine(path_to_input: str) -> collections.abc.Iterator[Machine]:
    with open(file=path_to_input) as f:
        for line in map(str.strip, f):
            yield Machine.from_line(line=line)


@aoc2025.expects(484)
def part_one(path_to_input: str) -> int:
    return sum(
        len(next(iter(iter_presses(buttons=machine.buttons, goal=machine.goal))))
        for machine in iter_machine(path_to_input=path_to_input)
    )


@aoc2025.expects(19210)
def part_two(path_to_input: str) -> int:
    return sum(
        min(
            map(
                len,
                iter_multipresses(buttons=machine.buttons, joltages=machine.joltages),
            )
        )
        for idx, machine in enumerate(iter_machine(path_to_input=path_to_input))
    )
