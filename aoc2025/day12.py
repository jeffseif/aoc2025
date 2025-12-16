import dataclasses
import functools
import typing

import aoc2025


@dataclasses.dataclass
class Present:
    idx: int
    shape: list[list[bool]]

    @classmethod
    def from_str(cls, s: str) -> typing.Self:
        idx_line, *shape_lines = s.splitlines()
        return cls(
            idx=int(idx_line[:-1]),
            shape=[[char == "#" for char in line.strip()] for line in shape_lines],
        )

    @functools.cached_property
    def area(self) -> int:
        return sum(char for row in self.shape for char in row)


@dataclasses.dataclass
class Tree:
    counts: list[int]
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> typing.Self:
        xy, _, counts = s.partition(": ")
        x, _, y = xy.partition("x")
        return cls(
            counts=list(map(int, counts.split())),
            x=int(x),
            y=int(y),
        )

    @functools.cached_property
    def area(self) -> int:
        return self.x * self.y


@dataclasses.dataclass
class Puzzle:
    presents: dict[int, Present]
    trees: list[Tree]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as f:
            content = f.read()
        *present_strs, tree_strs = content.split("\n\n")
        return cls(
            presents={
                present.idx: present for present in map(Present.from_str, present_strs)
            },
            trees=list(map(Tree.from_str, tree_strs.splitlines())),
        )


@aoc2025.expects(460)
def part_one(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    return sum(
        sum(puzzle.presents[idx].area * count for idx, count in enumerate(tree.counts))
        < tree.area
        for tree in puzzle.trees
    )


@aoc2025.expects(0)
def part_two(path_to_input: str) -> int:
    return 0
