from collections.abc import Iterator
from typing import Self

import pygame

from .config import Config
from .events import Compare, Event, Swap
from .sorting_algorithm import SortingAlgorithm
from .tiles import Tiles


class Visualizer:
    def __init__(self, config: Config) -> None:
        self._screen: pygame.Surface = pygame.display.set_mode((config.screen_width, config.screen_height))
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._config: Config = config

    def run(self, nums_to_sort: list[int], algorithm: SortingAlgorithm) -> None:
        screen_width, screen_height = self._screen.get_size()
        tiles: Tiles = Tiles(values=nums_to_sort, screen_width=screen_width, screen_height=screen_height)
        elapsed_since_reveal_ms: float = 0.0

        algo: Iterator[Event] = algorithm(nums_to_sort)

        while True:
            running = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not running:
                break

            while elapsed_since_reveal_ms >= self._config.update_time_ms:
                self._screen.fill("black")

                match next(algo):
                    case Swap(first, second):
                        tiles.swap(first, second)
                    case Compare(first, second):
                        tiles.highlight(first, second)
                    case other_step:
                        raise ValueError(f"Unrecognized event: {other_step}")

                for idx, tile in enumerate(tiles):
                    tile.draw(self._screen, tile.width * idx)
                elapsed_since_reveal_ms -= self._config.update_time_ms

            pygame.display.flip()
            frame_time = self._clock.tick(self._config.fps)
            elapsed_since_reveal_ms += frame_time

    def _play_sort_verification(self):...

    def __enter__(self) -> Self:
        pygame.init()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
       pygame.quit()
