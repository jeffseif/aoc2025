import collections
import collections.abc
import dataclasses
import functools
import operator
import typing

import aoc2025


@dataclasses.dataclass
class DAG:
    edges: dict[str, list[str]]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        edges: dict[str, list[str]] = collections.defaultdict(list)
        with open(file=path_to_input) as f:
            for line in f:
                parent, _, children = line.partition(":")
                edges[parent].extend(child.strip() for child in children.split())
        return cls(edges=edges)

    def count_all_walks(self, start: str, end: str) -> int:
        @functools.cache
        def count_walks(
            start: str,
            end: str,
        ) -> int:
            if start == end:
                return 1
            else:
                return sum(
                    count_walks(start=child, end=end) for child in self.edges[start]
                )

        return count_walks(start=start, end=end)


@aoc2025.expects(696)
def part_one(path_to_input: str) -> int:
    dag = DAG.from_path_to_input(path_to_input=path_to_input)
    return dag.count_all_walks(
        start="you",
        end="out",
    )


@aoc2025.expects(473741288064360)
def part_two(path_to_input: str) -> int:
    dag = DAG.from_path_to_input(path_to_input=path_to_input)
    return functools.reduce(
        operator.mul,
        (
            dag.count_all_walks(
                start="svr",
                end="fft",
            ),
            dag.count_all_walks(
                start="fft",
                end="dac",
            ),
            dag.count_all_walks(
                start="dac",
                end="out",
            ),
        ),
    )
