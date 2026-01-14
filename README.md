# Tetris

This repository contains an implementation of the game Tetris written in Python (3.12) using [pygame](https://www.pygame.org).

## File Structure

- `app.py` — launcher and main app entry point. Initializes the game interface and runs the game loop.
- `src/` — Python source files:
	- `interface.py` — Rendering, input and event handling, UI and audio.
	- `state.py` — Board occupancy, scoring, level progression, contact detection.
	- `tile.py` — Tetromino logic: shapes, rotation, movement, collision checks, and queueing.
	- `button.py` — Simple UI button helper used in pause/resume menu.
	- `parameters.py` — Centralized configuration constants (colors, sizes, key bindings, timing constants etc.).

## How the Code Works (High Level)

The `GameInterface` (`src/interface.py`) class acts as the central components manager and provides functions to run the game loop, which renders the game scene every frame while also playing music and sound effects. 

When an object of `GameInterface` is created, instances of `Tile` (`src/tile.py`) and `GameState` (`src/state.py`)  and `Button` (`src/button.py`) are also automatically generated. 

`GameState` tracks the current game status, e.g. how the board is occupied, what is the current level, score and number of completed lines etc., while `Tile` represents the currently falling tetromino and handles its position, movement, rotation, collisions and queueing. The observer design pattern is used to handle the communication from these classes to `GameInterface` (e.g. for sound effects timing). The game can also be paused and `Button` is a generic helper class needed to define its logic and status.

## Running the Game

### Using a Python Virtual Environment

1. Create a Python 3 virtual environment and install dependencies (pygame):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip pygame
```

2. Run the app:

```bash
python3 app.py
```

### Directly From Source Files

TODO

### Download and Run the Latest Release

TODO

Controls are mapped in `src/parameters.py` (default: arrow keys for movement/rotation, SPACE for hard drop, ESC to pause).

## Notes for contributors

- Docstrings follow a lightweight `@param` / `@returns` tag format used across `src/`.
- Configuration constants live in `src/parameters.py` for easy tuning (colors, sizes, timings).
- If you change public APIs, update docstrings and add a small test or manual verification step.

## Troubleshooting

- If pygame fails to import, ensure your virtualenv has pygame installed and your Python version is compatible.
- For simple syntax checks, run:

```bash
python3 -m py_compile app.py src/*.py
```

## Code Documentation (Doxygen)

This repository includes a `Doxyfile`. To regenerate the HTML documentation install Doxygen and locally run:

```bash
doxygen doxygen/Doxyfile
```

Generated HTML is written to `doxygen/html/`. To view the documentation open the `index.html` file using a browser of your choice.

## References

- Pygame documentation: https://www.pygame.org/docs/
- Official Tetris Website: https://tetris.com/
- Tetris Wiki: https://tetris.wiki/Tetris.wiki

## Quick Roadmap

- Add a GitHub action that makes exectutables for Windows and Linux
- Make the first official release
- Add some new features to the game like controller support, leaderboard, controls menu, etc.
