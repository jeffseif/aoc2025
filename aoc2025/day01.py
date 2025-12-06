import collections.abc
import dataclasses
import typing

import aoc2025


@dataclasses.dataclass
class Knob:
    position: int
    zeros: int = 0

    def rotate(self, rotation: int) -> typing.Self:
        previous, current = self.position, self.position + rotation
        zeros = int(abs(current // 100 - previous // 100))
        if rotation < 0:
            if current % 100 == 0:
                zeros += 1
            if previous == 0:
                zeros -= 1
        return dataclasses.replace(
            self,
            position=current % 100,
            zeros=self.zeros + zeros,
        )


def iter_rotations(path_to_input: str) -> collections.abc.Iterator[int]:
    with open(file=path_to_input) as f:
        for line in f:
            left_or_right, value = line[:1], int(line[1:])
            sign = +1 if left_or_right == "R" else -1
            yield sign * value


@aoc2025.expects(1191)
def part_one(path_to_input: str) -> int:
    knob = Knob(position=50)
    password = 0
    for rotation in iter_rotations(path_to_input=path_to_input):
        knob = knob.rotate(rotation=rotation)
        password += knob.position == 0
    return password


@aoc2025.expects(6858)
def part_two(path_to_input: str) -> int:
    knob = Knob(position=50)
    for rotation in iter_rotations(path_to_input=path_to_input):
        knob = knob.rotate(rotation=rotation)
    return knob.zeros
