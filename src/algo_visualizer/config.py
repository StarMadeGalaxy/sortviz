from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Config:
    fps: int = 60

    # Controls how many screen updates are going to happen per second
    updates_per_second: int = 10

    # The amount of numbers(tiles) to be drawn
    number_count: int = 70
    number_max: int = 100
    number_min: int = 1

    screen_height: int = 720
    screen_width: int = 1280

    # Time's taken for an update in milliseconds, NOT the same as frame time
    @property
    def update_time_ms(self) -> float:
        return 1000 / self.updates_per_second
