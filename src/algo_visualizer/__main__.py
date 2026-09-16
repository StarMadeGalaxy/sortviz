from typing import Self
import random

import pygame


NUMBER_COUNT: int = 70      # The amount of numbers in the list to be sorted
NUMBER_MAX: int = 100
NUMBER_MIN: int = 1
FPS: int = 60
UPDATES_PER_SECOND: int = 1   # Controls how many screen updates are going to be happen per second
# Time's taken for an update in milliseconds, NOT the same as frame time
UPDATE_TIME_MS: float = 1000 / UPDATES_PER_SECOND


class Tile:
    max_value: int = 0
    min_value: int = 0
    screen_height: int = 0
    width: float = 0      # all of the tiles are the same width
    num_of_tiles_shown: int = 0     # shows how many tiles are shown

    def __init__(self, index: int, value: int, color: pygame.Color | None = None):
        self.index = index
        self.value = value
        self.color = Tile.random_color() if color is None else color
        self.height = int(Tile.screen_height * value / Tile.max_value)

    def draw(self, screen: pygame.Surface) -> None:
        x = self.index * Tile.width
        y = Tile.screen_height - self.height
        rect_value = pygame.Rect(x, y, Tile.width, self.height)
        pygame.draw.rect(screen, self.color, rect_value)

    @staticmethod
    def swap(tiles: list["Tile"], first: int, second: int) -> None:
        tiles[first], tiles[second] = tiles[second], tiles[first]
        tiles[first].index, tiles[second].index = tiles[second].index, tiles[first].index

    @classmethod
    def create_tiles(cls, screen: pygame.Surface, nums: list, debug: bool=False) -> list[Self]:
        cls.max_value = max(nums)
        cls.min_value = min(nums)
        cls.screen_height = screen.get_height()
        cls.width = screen.get_width() / len(nums)
        return [cls(index, num) for index, num in enumerate(nums)]

    @staticmethod
    def random_color() -> pygame.Color:
        return pygame.Color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    nums_to_sort = [random.randint(NUMBER_MIN, NUMBER_MAX) for _ in range(NUMBER_COUNT)]
    tiles: list[Tile] = Tile.create_tiles(screen, nums_to_sort, debug=True)

    elapsed_since_reveal_ms: float = 0.0

    while True:
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break


        time_for_update: float = UPDATE_TIME_MS
        while elapsed_since_reveal_ms >= time_for_update:
            print(elapsed_since_reveal_ms)
            Tile.swap(tiles, 0, -1)
            screen.fill("black")
            for tile in tiles:
                tile.draw(screen)
            elapsed_since_reveal_ms -= time_for_update

        pygame.display.flip()
        frame_time = clock.tick(FPS)
        elapsed_since_reveal_ms += frame_time

    pygame.quit()
