# sortviz

A Python/Pygame sorting visualizer. Requires Python 3.13+.

Application code handwritten by the author.

## Installation

Clone or download the repository, then run these commands from its root.

### With uv

```sh
uv sync
uv run sortviz
```

### With Python, venv and pip

Use a Python 3.13+ interpreter to create a virtual environment:

```sh
python -m venv .venv
```

Activate it on macOS/Linux:

```sh
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install and run:

```sh
python -m pip install .
sortviz
```

For development or source-based configuration, use `python -m pip install -e .`
instead. `uv sync` installs the project in editable mode.

## Usage

Run `uv run sortviz` with uv, or `sortviz` in the activated environment.
Module execution is also supported: `python -m sortviz` or
`uv run python -m sortviz`.

The application generates random integers and visualizes the selected algorithm.
Close the window to exit.

## Configuration

`Config` in `src/sortviz/config.py` holds runtime settings. Set keyword arguments
in the `Config(...)` call in `src/sortviz/__main__.py` before launching:

```python
config = Config(
    fps=60,
    updates_per_second=200,
    number_count=130,
    sorting_algorithm="bubble_sort",
)
```

| Field | Class default | Purpose |
| --- | --- | --- |
| `fps` | `60` | Frame-rate limit. |
| `updates_per_second` | `10` | Rate at which algorithm events are consumed. |
| `number_count` | `70` | Number of generated values and displayed tiles. |
| `number_min` | `1` | Inclusive lower bound for generated integers. |
| `number_max` | `100` | Inclusive upper bound for generated integers. |
| `screen_width` | `1280` | Window width in pixels. |
| `screen_height` | `720` | Window height in pixels. |
| `sorting_algorithm` | `"bubble_sort"` | Registered algorithm name. |

The entry point overrides the update rate to `200` and input size to `130`.
`update_time_ms` is a derived property (`1000 / updates_per_second`), not a
constructor argument. `Config` is immutable after construction.

Algorithm selection uses `ALGORITHMS[config.sorting_algorithm]`. Set
`sorting_algorithm` to a registered name; the built-in name is `bubble_sort`.
Configuration is set in Python, with no command-line flags. After source changes,
restart the application; reinstall first if using a non-editable installation.

## Architecture

- **Algorithms** own sorting logic and mutate the input list, yielding semantic
  events that describe their operations independently of presentation.
- **Events** form the contract between algorithms and visualization.
- **Visualizer** consumes events and owns timing, the Pygame event loop and
  rendering coordination.
- **Tiles** maintains a separate visual collection, including layout, colors and
  visual updates. Each **Tile** draws itself on a Pygame surface.
- **Config** holds runtime parameters; the **registry** maps names to algorithms.
- **The entry point** loads algorithms, creates configuration and random input,
  selects an implementation and starts the visualizer.

Algorithms do not perform rendering, timing or Pygame operations.

## Adding an algorithm

1. Create `src/sortviz/algorithm/my_sort.py`. Follow the `SortingAlgorithm`
   contract: accept `nums: list[int]`, sort it in place and yield `Event` values
   through an `Iterator[Event]`. See `algorithm/bubble_sort.py` for an implementation.

2. Import the registration decorator and decorate your generator with a unique
   name:

   ```python
   from collections.abc import Iterator

   from ..events import Event
   from ..registry import register

   @register("my_sort")
   def my_sort(nums: list[int]) -> Iterator[Event]:
       # Implement sorting here, yielding events for its operations.
       ...
   ```

   This is a signature template; the implementation must contain `yield`.
   Supported events are defined in `events.py`: yield `Compare(i, j)` before a
   comparison and `Swap(i, j)` after exchanging the corresponding list elements.
   Indices refer to the current list positions. The visualizer applies exchanges
   to its separate tile collection. To introduce another semantic operation, add
   its event type to `Event` and handle it in `Visualizer.run`.

3. Import the module in `src/sortviz/algorithm/__init__.py`:

   ```python
   from . import my_sort as my_sort
   ```

   Registration runs when the module is imported. The entry point imports this
   package before looking up an algorithm; creating a file alone does not register
   it. The first registration for a name is retained.

4. Set `sorting_algorithm="my_sort"` in the entry point's `Config(...)` call,
   then launch the application.
