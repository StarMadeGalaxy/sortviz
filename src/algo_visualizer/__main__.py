from typing import Self
import random

import pygame



NUMBER_COUNT: int = 70      # The amount of numbers in the list to be sorted
NUMBER_MAX: int = 100
NUMBER_MIN: int = 1
FPS: int = 60
TILES_PER_SECOND: int = 5   # Controls how many tiles are going to be drawn per second


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

    def swap(self, swap_with: Self) -> None:
        self.color, swap_with.color = swap_with.color, self.color
        self.index, swap_with.index = swap_with.index, self.index
        self.value, swap_with.value = swap_with.value, self.value
        self.height, swap_with.height = swap_with.height, self.height
        pass

    @classmethod
    def init(cls, screen: pygame.Surface, nums: list, debug: bool=False) -> None:
        cls.max_value = max(nums)
        cls.min_value = min(nums)
        cls.screen_height = screen.get_height()
        cls.width = screen.get_width() / len(nums)

        if debug:
            print(f"Screen width: {screen.get_width()}")
            print(f"Tile width: {Tile.width}")
            print(f"Number of tiles: {NUMBER_COUNT}")

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
    running = True
    clock = pygame.time.Clock()
    nums_to_sort = [random.randint(NUMBER_MIN, NUMBER_MAX) for _ in range(NUMBER_COUNT)]
    Tile.init(screen, nums_to_sort, debug=True)
    tiles: list[Tile] = [Tile(index, num) for index, num in enumerate(nums_to_sort)]

    elapsed_since_reveal_ms: float = 0.0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time_for_tile: float = 1000 / TILES_PER_SECOND
        while elapsed_since_reveal_ms >= time_for_tile:
            if Tile.num_of_tiles_shown == NUMBER_COUNT:
                screen.fill("black")
                Tile.num_of_tiles_shown = 0

            tiles[Tile.num_of_tiles_shown].draw(screen)
            Tile.num_of_tiles_shown += 1

            elapsed_since_reveal_ms -= time_for_tile

        pygame.display.flip()
        frame_time = clock.tick(FPS)
        elapsed_since_reveal_ms += frame_time

    pygame.quit()
