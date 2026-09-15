import pygame

import random


NUMBER_COUNT: int = 70      # The amount of numbers in the list to be sorted
NUMBER_MAX: int = 100
NUMBER_MIN: int = 1
SAMPLE_RATE: int = 44100    # Samples describing each second of audio
TONE_FREQUENCY = 440   # Wave repetitions per second: pitch in Hz
FPS: int = 60
TILES_PER_SECOND: int = 1   # Controls how many tiles are going to be drawn per second

class Tile:
    max_value: int = 0
    min_value: int = 0
    screen_height: int = 0
    width: float = 0      # all of the tiles are the same width
    num_of_tiles_shown: int = 0     # shows how many tiles are shown

    def __init__(self, value: int, color: pygame.Color):
        self.value = value
        self.color = color
        self.height = int(Tile.screen_height * value / Tile.max_value)
        self.sound_frequency = TONE_FREQUENCY * self.value / Tile.max_value

    def draw(self, screen: pygame.Surface, index: int) -> None:
        x = index * Tile.width
        y = Tile.screen_height - self.height
        rect_value = pygame.Rect(x, y, Tile.width, self.height)
        pygame.draw.rect(screen, self.color, rect_value)

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

# don't understand the code its CODEX CODE
def test_sound(frequency: float, duration_sec: float) -> None:
    import numpy as np

    DURATION = 0.1         # Seconds
    VOLUME = 0.15          # Fraction of maximum amplitude

      # 1. Give every sample a time position, measured in seconds.
    sample_count = int(SAMPLE_RATE * DURATION)
    times = np.arange(sample_count) / SAMPLE_RATE

    # 2. Calculate a sine wave at those times.
    # One complete wave cycle corresponds to 2*pi radians.
    wave = np.sin(2 * np.pi * frequency * times)

    # 3. Fade the beginning and end to avoid abrupt clicks.
    fade_count = int(SAMPLE_RATE * 0.01)  # 10 milliseconds
    wave[:fade_count] *= np.linspace(0, 1, fade_count)
    wave[-fade_count:] *= np.linspace(1, 0, fade_count)

    # 4. Convert amplitudes from approximately -1...1
    # into the integer format expected by the mixer.
    samples = (wave * VOLUME * 32767).astype(np.int16)

    # 5. Turn the samples into a sound and play it.
    sound = pygame.sndarray.make_sound(samples)
    sound.play()

    # Keep this standalone example alive until playback finishes.
    pygame.time.wait(int(sound.get_length() * 1000) + 100)

def main() -> None:
    # One audio channel (mono), using signed 16-bit samples.
    pygame.mixer.init(
        frequency=SAMPLE_RATE,
        size=-16,
        channels=1,
    )

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    running = True
    clock = pygame.time.Clock()
    nums_to_sort = [random.randint(NUMBER_MIN, NUMBER_MAX) for _ in range(NUMBER_COUNT)]
    Tile.init(screen, nums_to_sort, debug=True)
    tiles: list[Tile] = [Tile(num, Tile.random_color()) for num in nums_to_sort]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                raise SystemExit

        screen.fill("black")
        for index, tile in enumerate(tiles):
            if Tile.num_of_tiles_shown == NUMBER_COUNT:
                Tile.num_of_tiles_shown = 0
            tile.draw(screen, index)
            Tile.num_of_tiles_shown += 1
            print(Tile.num_of_tiles_shown)
            #test_sound(tile.sound_frequency, duration_sec=0.01)

        pygame.display.flip()
        what = clock.tick(FPS)
        print(what)

    pygame.mixer.quit()
    pygame.quit()
