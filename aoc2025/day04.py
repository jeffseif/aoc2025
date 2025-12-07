import dataclasses
import functools
import typing

import aoc2025


@dataclasses.dataclass
class Grid:
    nodes: list[list[bool]]

    @classmethod
    def from_path_to_inputs(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as f:
            return cls(nodes=[[char == "@" for char in line] for line in f])

    @functools.cached_property
    def size(self) -> int:
        return len(self.nodes)

    def get_neighbors_inclusive(self, idx: int, jdx: int) -> list[bool]:
        return [
            self.nodes[i][j]
            for i in range(idx - 1, idx + 2)
            for j in range(jdx - 1, jdx + 2)
            if 0 <= i < self.size
            if 0 <= j < self.size
        ]

    @property
    def removables(self) -> list[tuple[int, int]]:
        return [
            (idx, jdx)
            for idx in range(self.size)
            for jdx in range(self.size)
            if self.nodes[idx][jdx]
            if sum(self.get_neighbors_inclusive(idx=idx, jdx=jdx)) <= 4
        ]

    def remove(self, idx: int, jdx: int) -> None:
        assert self.nodes[idx][jdx]
        self.nodes[idx][jdx] = False
        return None


@aoc2025.expects(1578)
def part_one(path_to_input: str) -> int:
    grid = Grid.from_path_to_inputs(path_to_input=path_to_input)
    return len(grid.removables)


@aoc2025.expects(10132)
def part_two(path_to_input: str) -> int:
    grid = Grid.from_path_to_inputs(path_to_input=path_to_input)
    removed = 0
    while removables := grid.removables:
        for idx, jdx in removables:
            grid.remove(idx=idx, jdx=jdx)
        removed += len(removables)
    return removed
