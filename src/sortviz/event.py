from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Compare:
    first: int
    second: int

@dataclass(frozen=True, slots=True)
class Swap:
    first: int
    second: int

type Event = Compare | Swap
