FPS = 60
MS_PER_S = 1000
GRID_ELEM_SIZE = 30
GRID_NR_OF_COLS = 10
GRID_NR_OF_ROWS = 20
# TLC = top left corner
GRID_TLC_x = 50
GRID_TLC_y = 50
GAME_WINDOW_WIDTH = 900
GAME_WINDOW_HEIGHT = 680
BACKGROUND_POS = (-830, -320)
LOGO_POS = (-100, -130)
FALL_TIME_INTERVAL_ms = 1000

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128,128,128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)

TILE_COLORS = {"I": CYAN,
               "J": BLUE,
               "L": ORANGE,
               "O": YELLOW,
               "S": GREEN,
               "T": PURPLE,
               "Z": RED}

TILE_SHAPES = {"I": [[[1, 1, 1, 1],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0]],
                     
                     [[1, 1, 1, 1],
                     [0, 0, 0, 0],
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
               
                "L": [[[1, 1, 1, 0],
                     [1, 0, 0, 0],
                     [0, 0, 0, 0],
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
                
                "S": [[[0, 1, 1, 0],
                     [1, 1, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 1, 0],
                     [1, 1, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],
                
                "T": [[[1, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [1, 1, 1, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 1, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],
                
                "Z": [[[1, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[1, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]],
                     
                     [[0, 0, 1, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]]
                     ],                                                      
               }

NR_OF_TILES = len(TILE_SHAPES)
TILE_CONFIG_IDX_MAX = 4