import collections.abc

import aoc2025


def iter_fresh_ingredients(path_to_input: str) -> collections.abc.Iterator[int]:
    fresh_spans = []

    with open(file=path_to_input) as f:
        for line in f:
            if line == "\n":
                break
            fresh_spans.append(tuple(map(int, line.split("-"))))
        for ingredient in map(int, f):
            for lower, upper in fresh_spans:
                if lower <= ingredient <= upper:
                    yield ingredient
                    break


def spans_overlap(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[1] >= right[0] and right[1] >= left[0]


def get_collapsed(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    collapsed: list[tuple[int, int]] = []
    for span in sorted(spans):
        try:
            idx, overlapping = next(
                (idx, overlapping)
                for idx, overlapping in enumerate(collapsed)
                if spans_overlap(left=span, right=overlapping)
            )
        except StopIteration:
            collapsed.append(span)
        else:
            collapsed[idx] = (min(overlapping), max(overlapping[1], span[1]))
    return collapsed


def iter_fresh_id_counts(path_to_input: str) -> collections.abc.Iterator[int]:
    spans: list[tuple[int, int]] = []
    with open(file=path_to_input) as f:
        for line in f:
            if line == "\n":
                break
            spans.append(tuple(map(int, line.split("-"))))  # type: ignore
    while len(spans) > len(spans := get_collapsed(spans=spans)):
        ...
    for lower, upper in spans:
        yield upper - lower + 1


@aoc2025.expects(509)
def part_one(path_to_input: str) -> int:
    return aoc2025.count(iter_fresh_ingredients(path_to_input=path_to_input))


@aoc2025.expects(336790092076620)
def part_two(path_to_input: str) -> int:
    return sum(iter_fresh_id_counts(path_to_input=path_to_input))
