from collections.abc import Callable

from .sorting_algorithm import SortingAlgorithm

ALGORITHMS: dict[str, SortingAlgorithm] = {}


def register(function_name: str) -> Callable[[SortingAlgorithm], SortingAlgorithm]:
    def wrap(func: SortingAlgorithm) -> SortingAlgorithm:
        if function_name in ALGORITHMS:
            raise ValueError(f"Function {function_name!r} is already registered.")
        else:
            ALGORITHMS[function_name] = func
        return func
    return wrap
