# Tetris (minimal Python implementation)

A small Tetris implementation written in Python (3.12) using [pygame](https://www.pygame.org). This repository contains the game logic, rendering, and configuration used to run a playable Tetris game.

## Layout / key files

- `app.py` — launcher and main app entry point. Initializes the game interface and runs the game loop.
- `src/` — Python source files:
	- `interface.py` — Rendering, input handling, UI (pause menu, stats display) and audio.
	- `state.py` — Game state: board occupancy, scoring, level progression, contact detection and event dispatching.
	- `tile.py` — Tetromino logic: shapes, rotation, movement, collision checks, and queueing.
	- `button.py` — Simple UI button helper used in pause/resume menu.
	- `parameters.py` — Centralized configuration constants (colors, sizes, key bindings, timing constants etc.).

## How it works (high level)

- The `GameInterface` in `src/interface.py` creates a `GameState` and a `Tile` manager. It handles pygame events, draws the playfield and UI, and controls timing (tick/soft-drop events).
- `GameState` stores the board occupancy matrix, handles collision/contact detection, cleared-row deletion, scoring rules, and emits events (e.g., `hard_drop`, `game_paused`).
- `Tile` represents the active tetromino, reads shape matrices from `parameters.py`, performs rotation/wall-kick checks, computes drop distances, and notifies `GameState` when it locks.

## Run (development)

1. Create a Python 3 virtual environment and install dependencies (pygame):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip pygame
```

2. Run the game:

```bash
python3 app.py
```

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

## Doxygen

This repository includes a `doxygen/Doxyfile`. To regenerate the HTML documentation install Doxygen and locally run:

```bash
doxygen doxygen/Doxyfile
```

Generated HTML is written to `doxygen/html/`. To view the documentation open the `index.html` file using a browser.

## References

- Pygame documentation: https://www.pygame.org/docs/

## Quick roadmap

- Add a GitHub action that makes exectutables for Windows and Linux
- Make the first official release
- Add some new features to the game like controller support, leaderboard, controls menu, etc.
