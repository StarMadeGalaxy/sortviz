from collections.abc import Iterator
from typing import Protocol

from sortviz.algorithm.event import Event


class SortingAlgorithm(Protocol):
    def __call__(self, nums_to_sort: list[int]) -> Iterator[Event]:
        ...
