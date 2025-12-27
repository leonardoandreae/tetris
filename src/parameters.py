import pygame as pyg

# Miscellaneous

## Target frames per second used by the main loop / clock tick.
TARGET_FPS = 60
## Initial interval (ms) between automatic tile falls (gravity).
INITIAL_FALL_TIME_INTERVAL_ms = 500
## Timeout (ms) used to confirm down contact before locking a tile.
DOWN_CONTACT_TIMEOUT_ms = 500
## How much the fall interval is reduced when leveling up (ms).
FALL_TIME_INTERVAL_DELTA_ms = 40
## Interval (ms) used for the soft-drop timer event.
SOFT_DROP_TIME_INTERVAL_ms = 80
## Thickness (px) of the border drawn around each block when rendering.
BLOCK_BORDER_THICKNESS = 2
## Border thickness (px) for the preview of where a dropped block will land.
DROPPED_BLOCK_PREVIEW_BORDER = 2
## Primary font size used for UI text.
FONT_SIZE_1 = 22
## Secondary font size used for UI text.
FONT_SIZE_2 = 22
## Global music volume (0.0 - 1.0).
MUSIC_VOLUME = 0.5
## Number of upcoming tiles queued ahead of the current tile.
TILE_QUEUE_SIZE = 5
## Milliseconds of cooldown between pause/resume toggles.
PAUSE_COOLDOWN_ms = 300
## Maximum playable level.
MAX_LEVEL = 10
## Number of lines required per level increment.
MAX_LINES_PER_LEVEL = 10

# Score related

## Score multipliers applied per number of cleared lines at once.
LINE_CLEAR_SCORE_MULTIPLIERS = {
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}
## Multiplier applied to hard-drop score calculation.
SCORE_MULTIPLIER_HARD_DROP = 2

## Default UI button font size (px).
DEFAULT_BUTTON_FONT_SIZE = 40
## Default UI button corner radius (px) for rounded rectangles.
DEFAULT_BUTTON_BORDER_RADIUS = 20
## Spacing (px) between button text and the button border.
TEXT_TO_BUTTON_BORDER_SPACING = 30
## Default on-screen position for the resume button (used in the pause menu).
RESUME_BUTTON_POS = (350, 300)

## Game window default width in pixels.
GAME_WINDOW_WIDTH = 900
## Game window default height in pixels.
GAME_WINDOW_HEIGHT = 680
## On-screen coordinates where the game logo is blitted.
LOGO_POS = (450, 50)
## Scale factor applied to the logo image when rendering.
LOGO_SCALE_FACTOR = 1.5
## Base position used to render the statistics (score/level/lines).
STATS_POS = (660, 375)
## Vertical spacing (px) between statistics text lines.
STATS_VERTICAL_SPACING = 10
## Position for the "Next" piece label text (pygame Vector2).
NEXT_PIECE_TEXT_POS = pyg.Vector2(480, 330)
## Top-left position for the small next-piece 4x4 preview grid (pygame Vector2).
NEXT_PIECE_GRID_POS = pyg.Vector2(450, 360)
## Position at which to blit the semi-transparent pause overlay.
PAUSE_MENU_TRANSPARENT_OVERLAY_POS = (0, 0)
## Position for pause information text (pygame Vector2).
PAUSE_INFO_TEXT_POS = pyg.Vector2(450, 600)

## Red color (RGB).
RED = (255, 0, 0)
## Black color (RGB).
BLACK = (0, 0, 0)
## White color (RGB) used as primary foreground.
WHITE = (255, 255, 255)
## Grey color used for grid lines and outlines.
GREY = (128,128,128)
## Cyan color used for the I tetromino.
CYAN = (0, 255, 255)
## Yellow color used for the O tetromino.
YELLOW = (255, 222, 33)
## Purple color used for the T tetromino.
PURPLE = (128, 0, 128)
## Green color used for the S tetromino.
GREEN = (0, 255, 0)
## Blue color used for the J tetromino.
BLUE = (0, 0, 255)
## Orange color used for the L tetromino.
ORANGE = (255, 127, 0)
## Semi-transparent grey (RGBA) used for overlays like pause.
TRANSPARENT_GREY = (128, 128, 128, 150)
## Default button color mapping (idle, hover, active states).
DEFAULT_BUTTON_COLORS = {"button_idle": WHITE,
                         "button_hover": YELLOW,
                         "button_active": GREEN}

## Size (px) for one grid cell / block.
GRID_ELEM_SIZE = 30
## Number of columns in the main playfield grid.
GRID_NR_OF_COLS = 10
## Number of rows in the main playfield grid.
GRID_NR_OF_ROWS = 20
## X coordinate (px) of the top-left corner of the playfield grid.
GRID_TLC_x = 50
## Y coordinate (px) of the top-left corner of the playfield grid.
GRID_TLC_y = 50
## Line thickness for the grid lines (px).
GRID_THICKNESS = 2
## Default color used when drawing empty grid cells / outlines.
DEFAULT_GRID_COLOR = WHITE

## Mapping from tetromino type to its display color.
TILE_COLORS = {"I": CYAN,
               "J": BLUE,
               "L": ORANGE,
               "O": YELLOW,
               "S": GREEN,
               "T": PURPLE,
               "Z": RED}

## Maximum number of rotation configurations per tile (standard 4).
TILE_CONFIG_IDX_MAX = 4
## Shape configurations for each tetromino type. Each value is a list of 4 matrices (4x4) representing the rotation states.
TILE_SHAPES = {"I": [[[0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0]],
                     
                     [[0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0]]
                     ],
               
               "J": [[[0, 0, 0, 0],
                     [1, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [1, 0, 0, 0],
                     [1, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],
               
                "L": [[[0, 0, 0, 0],
                     [1, 1, 1, 0],
                     [1, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [0, 0, 1, 0],
                     [1, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],
                
                "O": [[[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]]
                     ],
                
                "S": [[[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [1, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [1, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],
                
                "T": [[[0, 0, 0, 0],
                     [1, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],
                
                "Z": [[[0, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],                                                      
               }

# Hotkeys

## Key mapping for move left.
LEFT = pyg.K_LEFT
## Key mapping for move right.
RIGHT = pyg.K_RIGHT
## Key mapping for soft drop.
DOWN = pyg.K_DOWN
## Key mapping for rotate action.
ROTATE = pyg.K_UP
## Key mapping for hard drop.
HARD_DROP = pyg.K_SPACE
## Key mapping for pause/resume.
PAUSE = pyg.K_ESCAPE