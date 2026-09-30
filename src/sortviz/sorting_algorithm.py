from collections.abc import Iterator
from typing import Protocol

from .events import Event


class SortingAlgorithm(Protocol):
    def __call__(self, nums: list[int]) -> Iterator[Event]:
        ...
