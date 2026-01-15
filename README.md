# Tetris ![Build](https://github.com/leonardoandreae/tetris/actions/workflows/release.yml/badge.svg)


This repository contains an implementation of the game Tetris written in Python (3.12) using [pygame](https://www.pygame.org).

## Key Files

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

`GameState` tracks the current game status, e.g. how the board is occupied, what is the current level, score and number of completed lines etc., while `Tile` represents the currently falling tetromino and handles its position, movement, rotation, collisions and queueing. The observer design pattern is used to handle the communication from these classes to `GameInterface` (e.g. for playing sound effects). The game can also be paused and `Button` is a generic helper class needed to define its logic and status.

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

### From Latest Release (Windows, MacOS and Linux)

[Latest Release Link](https://github.com/leonardoandreae/tetris/releases/latest)

##  Controls

Controls are mapped in `src/parameters.py` and can be reconfigured if needed. By default they are as follows:

- **Move Left:** ⬅️
- **Move Right:** ➡️
- **Rotate:** ⬆️
- **Soft Drop:** ⬇️
- **Hard Drop:** ⌨️ (Space)

## Code Documentation (Doxygen)

This repository includes a `Doxyfile`. To regenerate the HTML documentation install Doxygen and locally run:

```bash
doxygen doxygen/Doxyfile
```

The generated HTML is written to `doxygen/html/`. To view the documentation open the `index.html` file using a browser of your choice.

## References

- Pygame documentation: https://www.pygame.org/docs/
- Official Tetris Website: https://tetris.com/
- Tetris Wiki: https://tetris.wiki/Tetris.wiki

## Project Roadmap
- Add some new features to the game like controller support, leaderboard, controls menu, etc.
- Add controls viewing/changing menu
- Add leaderboard

## License & Copyright

© <CURRENT_YEAR> Leonardo Andreae. All rights reserved.

This project is licensed under the [MIT LICENSE](https://opensource.org/licenses/MIT)), which means you are free to use, modify, and distribute the software, provided that the original copyright notice and license are included in all copies or substantial portions of the software.

You may NOT claim this work as your own or redistribute it without proper attribution.

