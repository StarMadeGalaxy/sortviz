from collections.abc import Iterator

from ..events import Compare, Event, Swap
from ..registry import register


@register("Bubble Sort")
def bubble_sort(nums: list[int]) -> Iterator[Event]:
    for i in range(len(nums) - 1):
        for j in range(len(nums) - 1 - i):
            yield Compare(j, j+1)
            if nums[j] > nums[j+1]:
                nums[j+1], nums[j] = nums[j], nums[j+1]
                yield Swap(j+1, j)
