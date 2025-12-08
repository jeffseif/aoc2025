import collections
import collections.abc
import functools
import itertools
import operator

import aoc2025


def iter_xyz(
    path_to_input: str,
) -> collections.abc.Iterator[tuple[int, int, int]]:
    with open(file=path_to_input) as f:
        for line in f:
            yield tuple(map(int, line.split(",")))


def get_distance_squared(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> float:
    return sum((l - r) ** 2 for l, r in zip(left, right, strict=True))


@aoc2025.expects(181584)
def part_one(
    path_to_input: str, number_of_connections: int = 1_000, number_of_circuits: int = 3
) -> int:
    distances = {
        (left, right): get_distance_squared(left, right)
        for left, right in itertools.combinations(
            iter_xyz(path_to_input=path_to_input), 2
        )
    }
    xyz_to_group = {}
    group_to_xyzs = collections.defaultdict(set)
    for left, right in itertools.islice(
        sorted(distances, key=distances.__getitem__), number_of_connections
    ):
        if (left not in xyz_to_group) and (right not in xyz_to_group):
            xyz_to_group[left] = xyz_to_group[right] = group = (
                max(group_to_xyzs, default=0) + 1
            )
            group_to_xyzs[group].update((left, right))
        elif right not in xyz_to_group:
            xyz_to_group[right] = group = xyz_to_group[left]
            group_to_xyzs[group].add(right)
        elif left not in xyz_to_group:
            xyz_to_group[left] = group = xyz_to_group[right]
            group_to_xyzs[group].add(left)
        elif (left_group := xyz_to_group[left]) == (right_group := xyz_to_group[right]):
            ...
        else:
            for xyz in group_to_xyzs[right_group]:
                xyz_to_group[xyz] = left_group
            group_to_xyzs[left_group].update(group_to_xyzs.pop(right_group))
    return functools.reduce(
        operator.mul,
        itertools.islice(
            sorted(map(len, group_to_xyzs.values()), reverse=True), number_of_circuits
        ),
    )


@aoc2025.expects(8465902405)
def part_two(path_to_input: str) -> int:
    xyzs = list(iter_xyz(path_to_input=path_to_input))
    distances = {
        (left, right): get_distance_squared(left, right)
        for left, right in itertools.combinations(xyzs, 2)
    }
    xyz_to_group = {}
    group_to_xyzs = collections.defaultdict(set)
    for left, right in sorted(distances, key=distances.__getitem__):
        if (left not in xyz_to_group) and (right not in xyz_to_group):
            xyz_to_group[left] = xyz_to_group[right] = group = (
                max(group_to_xyzs, default=0) + 1
            )
            group_to_xyzs[group].update((left, right))
        elif right not in xyz_to_group:
            xyz_to_group[right] = group = xyz_to_group[left]
            group_to_xyzs[group].add(right)
        elif left not in xyz_to_group:
            xyz_to_group[left] = group = xyz_to_group[right]
            group_to_xyzs[group].add(left)
        elif (left_group := xyz_to_group[left]) == (right_group := xyz_to_group[right]):
            ...
        else:
            for xyz in group_to_xyzs[right_group]:
                xyz_to_group[xyz] = left_group
            group_to_xyzs[left_group].update(group_to_xyzs.pop(right_group))
        if len(xyz_to_group) == len(xyzs) and len(group_to_xyzs) == 1:
            (x1, _, _), (x2, _, _) = left, right
            return x1 * x2
    raise ValueError
