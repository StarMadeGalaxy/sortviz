from .sorting_algorithm import SortingAlgorithm

ALGORITHMS: dict[str, SortingAlgorithm] = {}

def register(func: SortingAlgorithm) -> None:
    def wrap(function_name: str) -> SortingAlgorithm:
        if function_name not in ALGORITHMS:
            ALGORITHMS[function_name] = func
        return func
