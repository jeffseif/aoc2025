import dataclasses
import enum
import typing

import aoc2025


class Node(enum.Enum):
    START = "S"
    SPLITTER = "^"
    EMPTY = "."
    BEAM = "|"


@dataclasses.dataclass
class ClassicManifold:
    rows: list[list[Node]]
    weights: list[list[int]]
    clock: int = 0
    splits: int = 0

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as f:
            rows = [list(map(Node.__call__, line)) for line in map(str.strip, f)]
            weights = [[0 for _ in row] for row in rows]
            first = weights[0]
            for idx in range(len(first)):
                first[idx] += 1
            return cls(
                rows=rows,
                weights=weights,
            )

    def __iter__(self) -> typing.Self:
        return self

    def __next__(self) -> typing.Self:
        self.clock += 1
        if self.clock == len(self.rows):
            raise StopIteration
        idxs = (
            idx
            for idx, node in enumerate(self.rows[self.clock - 1])
            if node in {Node.START, Node.BEAM}
        )
        for idx in idxs:
            weight = self.weights[self.clock - 1][idx]
            if self.rows[self.clock][idx] in {Node.SPLITTER}:
                self.splits += 1
                self.rows[self.clock][idx - 1] = self.rows[self.clock][idx + 1] = (
                    Node.BEAM
                )
                self.weights[self.clock][idx - 1] += weight
                self.weights[self.clock][idx + 1] += weight
            else:
                self.rows[self.clock][idx] = Node.BEAM
                self.weights[self.clock][idx] += weight
        return self


@aoc2025.expects(1499)
def part_one(path_to_input: str) -> int:
    manifold = ClassicManifold.from_path_to_input(path_to_input=path_to_input)
    aoc2025.exhaust(manifold)
    return manifold.splits


@aoc2025.expects(24743903847942)
def part_two(path_to_input: str) -> int:
    manifold = ClassicManifold.from_path_to_input(path_to_input=path_to_input)
    aoc2025.exhaust(manifold)
    return sum(manifold.weights[-1])
