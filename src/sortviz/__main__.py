import random

from .config import Config
from .registry import ALGORITHMS
from .visualizer import Visualizer


def main() -> None:
    config = Config(
        updates_per_second=200,
        number_count=130,
        sorting_algorithm="Bubble Sort"
    )
    print(ALGORITHMS)
    algorithm = ALGORITHMS[config.sorting_algorithm]

    nums_to_sort = [random.randint(config.number_min, config.number_max) for _ in range(config.number_count)]

    with Visualizer(config) as vis:
        vis.run(nums_to_sort, algorithm)
