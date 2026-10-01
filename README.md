````markdown
# sortviz

Sorting visualizer written in Python using Pygame.

Requires Python 3.13+.

Application code handwritten by the author.

## Installation

Clone the repository:

```sh
git clone https://github.com/YOUR_USERNAME/sortviz.git
cd sortviz
```

### With uv

Install the project and its dependencies:

```sh
uv sync
```

Run:

```sh
uv run sortviz
```

or:

```sh
uv run python -m sortviz
```

### Without uv

Create a virtual environment:

```sh
python -m venv .venv
```

Activate it.

macOS / Linux:

```sh
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project:

```sh
python -m pip install .
```

Run:

```sh
sortviz
```

or:

```sh
python -m sortviz
```

For development, install the package in editable mode:

```sh
python -m pip install -e .
```

## Usage

Run the application:

```sh
sortviz
```

or run the package as a module:

```sh
python -m sortviz
```

When using uv:

```sh
uv run sortviz
```

Algorithm selection is exposed through the command-line interface.

## Architecture

Sorting algorithms are generators. They modify the input sequence while yielding
semantic events such as `Compare` and `Swap`.

`Visualizer` consumes those events over time and owns the Pygame event loop,
timing, and application state.

`Tiles` owns the tile collection, dimensions, highlighting, swaps, and other
render-related state. Individual `Tile` objects draw themselves onto a Pygame
surface.

The algorithm registry maps public algorithm names to their implementations,
keeping algorithm selection separate from the visualizer.

`__main__.py` is the application entry point. It creates the input, selects the
sorting algorithm, configures the visualizer, and starts the application.

The general flow is:

```text
algorithm
    |
    | Compare / Swap / ...
    v
Visualizer
    |
    v
Tiles
    |
    v
Pygame
```

Sorting algorithms do not handle rendering or timing. They only perform the sort
and describe what happened through events.
```