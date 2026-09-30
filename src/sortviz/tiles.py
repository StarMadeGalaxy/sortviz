import random
from collections.abc import Iterator
from dataclasses import dataclass

import pygame


@dataclass(kw_only=True, slots=True)
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
    _HIGHLIGHT_COLOR: pygame.Color = pygame.Color(255, 0, 0)

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

    def swap(self, first: int, second: int) -> None:
        self._tiles[first], self._tiles[second] = self._tiles[second], self._tiles[first]

    def highlight(self, *indices: int) -> None:
        for index in indices:
            self._tiles[index].color = self._HIGHLIGHT_COLOR

    def _color_for_value(self, value, max_value) -> pygame.Color:
        red = random.randint(0, 255)
        green = int(255 * value / max_value)
        blue = random.randint(0, 255)
        return pygame.Color(red, green, blue)

    def __iter__(self) -> Iterator[Tile]:
        return iter(self._tiles)
