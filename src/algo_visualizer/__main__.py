from dataclasses import dataclass
from typing import Self
from collections.abc import Generator, Iterator
import random

import pygame

from .config import Config


def bubble_sort(nums: list[int]) -> Generator[tuple[int, int]]:
    yield (1, 2)


class Visualizer:
    def __init__(self, config: Config) -> None:
        self._screen: pygame.Surface = pygame.display.set_mode((config.screen_width, config.screen_height))
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._config: Config = config

    def run(self, nums_to_sort: list[int]) -> None:
        screen_width, screen_height = self._screen.get_size()
        tiles: Tiles = Tiles(values=nums_to_sort, screen_width=screen_width, screen_height=screen_height)

        elapsed_since_reveal_ms: float = 0.0
        while True:
            running = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not running:
                break

            while elapsed_since_reveal_ms >= self._config.update_time_ms:
                self._screen.fill("black")
                tiles.swap(0, -1)
                for idx, tile in enumerate(tiles):
                    tile.draw(self._screen, tile.width * idx)
                elapsed_since_reveal_ms -= self._config.update_time_ms

            pygame.display.flip()
            frame_time = self._clock.tick(self._config.fps)
            elapsed_since_reveal_ms += frame_time


    def __enter__(self) -> Self:
        pygame.init()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
       pygame.quit()


@dataclass(kw_only=True)
class Tile:
    value: int
    color: pygame.Color

    height: float
    width: float

    def draw(self, screen: pygame.Surface, x: float) -> None:
        y = screen.get_height() - self.height
        rect_value = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect_value)


class Tiles:
    def __init__(self, values: list[int], *, screen_height: int, screen_width: int) -> None:
        self._tiles: list[Tile] = []
        max_value = max(values)
        min_value = min(values)
        width = screen_width / len(values) # width of the single tile

        for idx, val in enumerate(values):
            temp_tile = Tile(
                value=val,
                color=self._color_for_value(val, max_value),
                height=screen_height * val / (max_value - min_value),
                width=width,
            )
            self._tiles.append(temp_tile)

    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)

    def swap(self, first: int, second: int) -> None:
        self._tiles[first], self._tiles[second] = self._tiles[second], self._tiles[first]

    def _color_for_value(self, value, max_value) -> pygame.Color:
        red = random.randint(0, 255)
        green = int(255 * value / max_value)
        blue = random.randint(0, 255)
        return pygame.Color(red, green, blue)



def main() -> None:
    config = Config()
    nums_to_sort = [random.randint(config.number_min, config.number_max) for _ in range(config.number_count)]

    with Visualizer(config) as vis:
        vis.run(nums_to_sort)
