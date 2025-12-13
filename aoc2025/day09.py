import collections.abc
import dataclasses
import itertools
import typing

import more_itertools

import aoc2025


T = typing.TypeVar("T")


@dataclasses.dataclass(frozen=True, order=True)
class Coord:
    x: int
    y: int

    @property
    def iter_neighbor(self) -> collections.abc.Iterator[Coord]:
        yield Coord(x=self.x + 1, y=self.y)
        yield Coord(x=self.x - 1, y=self.y)
        yield Coord(x=self.x, y=self.y + 1)
        yield Coord(x=self.x, y=self.y - 1)


def iter_rotation(
    it: collections.abc.Iterable[T],
) -> collections.abc.Iterator[tuple[T, T]]:
    ((first,), it) = more_itertools.spy(it, n=1)
    for previous, current in itertools.pairwise(it):
        yield (previous, current)
    yield (current, first)


def show(coords: list[Coord]) -> None:
    s = set(coords)
    print(
        "\n".join(
            "".join(
                "#" if Coord(x, y) in s else "."
                for x in range(max(c.x for c in coords) + 2)
            )
            for y in range(max(c.y for c in coords) + 2)
        )
    )
    return None


@dataclasses.dataclass
class Grid:
    coords: list[Coord]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        with open(file=path_to_input) as f:
            return cls(coords=[Coord(*map(int, line.split(","))) for line in f])

    @property
    def rectangle_to_area(self) -> dict[tuple[Coord, Coord], int]:
        def it() -> collections.abc.Iterator[tuple[tuple[Coord, Coord], int]]:
            for left, right in itertools.combinations(
                iterable=sorted(self.coords), r=2
            ):
                (xmin, xmax), (ymin, ymax) = (
                    sorted((left.x, right.x)),
                    sorted((left.y, right.y)),
                )
                yield ((left, right), (xmax - xmin + 1) * (ymax - ymin + 1))

        return dict(it())

    @property
    def filled_rectangle_to_area(self) -> dict[tuple[Coord, Coord], int]:
        x_to_idx = {x: i for i, x in enumerate(sorted({c.x for c in self.coords}))}
        y_to_idx = {y: j for j, y in enumerate(sorted({c.y for c in self.coords}))}
        coord_to_compressed = {
            coord: Coord(x=x_to_idx[coord.x], y=y_to_idx[coord.y])
            for coord in self.coords
        }
        compressed_to_coord = {
            compressed: coord for coord, compressed in coord_to_compressed.items()
        }

        def iter_border() -> collections.abc.Iterator[Coord]:
            for left, right in iter_rotation(
                map(coord_to_compressed.__getitem__, self.coords)
            ):
                dx = 0 if left.x == right.x else +1 if left.x < right.x else -1
                dy = 0 if left.y == right.y else +1 if left.y < right.y else -1
                step = left
                while step != right:
                    yield step
                    step = Coord(x=step.x + dx, y=step.y + dy)

        exterior = set(iter_border())

        def iter_flood() -> collections.abc.Iterator[Coord]:
            interior: set[Coord] = set()
            candidates = {
                coord
                for x in range(max(c.x for c in exterior))
                for y in range(max(c.y for c in exterior))
                if (coord := Coord(x=x, y=y)) not in exterior
                if all(neighbor in exterior for neighbor in coord.iter_neighbor)
            }
            if not candidates:
                candidates = {
                    Coord(
                        x=min(exterior).x + 1,
                        y=min(exterior).y + 1,
                    )
                }
            while candidates:
                if (candidate := candidates.pop()) not in exterior:
                    yield candidate
                    interior.add(candidate)
                    candidates.update(set(candidate.iter_neighbor) - interior)

        interior = set(iter_flood())

        valid = exterior | interior

        def it() -> collections.abc.Iterator[tuple[tuple[Coord, Coord], int]]:
            for left, right in itertools.combinations(
                iterable=map(coord_to_compressed.__getitem__, sorted(self.coords)), r=2
            ):
                (xmin, xmax), (ymin, ymax) = (
                    sorted((left.x, right.x)),
                    sorted((left.y, right.y)),
                )
                if all(
                    Coord(x=x, y=y) in valid
                    for x in range(xmin, xmax + 1)
                    for y in range(ymin, ymax + 1)
                ):
                    left, right = (
                        compressed_to_coord[left],
                        compressed_to_coord[right],
                    )
                    yield (
                        (left, right),
                        (abs(left.x - right.x) + 1) * (abs(left.y - right.y) + 1),
                    )

        return dict(it())


@aoc2025.expects(4748769124)
def part_one(path_to_input: str) -> int:
    grid = Grid.from_path_to_input(path_to_input=path_to_input)
    return max(grid.rectangle_to_area.values())


@aoc2025.skip_slow
@aoc2025.expects(1525991432)
def part_two(path_to_input: str) -> int:
    grid = Grid.from_path_to_input(path_to_input=path_to_input)
    return max(grid.filled_rectangle_to_area.values())
