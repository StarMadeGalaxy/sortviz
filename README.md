# sortviz

Sorting visualizer built with Python and Pygame. Uses uv for dependency management
and running the package. Requires Python 3.13+.

Application code handwritten by the author.

## Architecture

- Sorting algorithms are generators: they sort a list and yield semantic events
  such as `Compare` and `Swap`, without handling drawing or timing.
- `Visualizer` consumes those events over time and runs the Pygame loop.
- `Tiles` owns tile state, dimensions, colors, swaps, and highlights. Each `Tile`
  draws itself onto a Pygame surface.
- The registry is intended to map public algorithm names to implementations.
- `__main__.py` sets configuration, creates the input, and connects the algorithm
  to the visualizer.

Bubble sort is the current implementation. Work in progress: algorithm
registration is unfinished, so the default entry point cannot run yet.

## Run

Once registration is wired up:

```sh
uv sync
uv run sortviz
```
