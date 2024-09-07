import pygame as pyg

def update_tile_position():
    global x, y, ms_count, ms_count_prev
    keys_pressed = pyg.key.get_pressed()
    
    ms_count = pyg.time.get_ticks()  
    one_second_passed = (ms_count % 1000) < (ms_count_prev % 1000)
    
    if keys_pressed[pyg.K_LEFT]:
        if not keys_pressed[pyg.K_RIGHT]:
            x -= GRID_ELEM_SIZE
            
    if keys_pressed[pyg.K_RIGHT]:
        if not keys_pressed[pyg.K_LEFT]:
            x += GRID_ELEM_SIZE
    if one_second_passed:
        y += GRID_ELEM_SIZE
    
    ms_count_prev = ms_count
            
def draw_grid():
    for column in range(GRID_TLC_y, GRID_TLC_y+GRID_ELEM_SIZE*GRID_NR_OF_COLS, GRID_ELEM_SIZE):
        for row in range(GRID_TLC_x, GRID_TLC_x+GRID_ELEM_SIZE*GRID_NR_OF_ROWS, GRID_ELEM_SIZE):
            # create rectangle object
            grid_element = pyg.Rect(row, column, GRID_ELEM_SIZE, GRID_ELEM_SIZE)
            pyg.draw.rect(game_window, BLACK, grid_element, 1)

            
    
def update_scene():
    # color background such that older objects do not appear
    game_window.blit(BACKGROUND, (0, 0))
    
    draw_grid()
    
    # draw tile
    tile = pyg.Rect(x, y, GRID_ELEM_SIZE, GRID_ELEM_SIZE)
    pyg.draw.rect(game_window, RED, tile)
    # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
    pyg.display.update()
    
    
# define some parameters
FPS = 60
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_ELEM_SIZE = 20
GRID_NR_OF_COLS = 15
GRID_NR_OF_ROWS = 15
# TLC = top left corner
GRID_TLC_x = 50
GRID_TLC_y = 50

game_window_width = 1700
game_window_height = 1000

pyg.init()
game_window = pyg.display.set_mode((game_window_width, game_window_height))
pyg.display.set_caption("Tetris")

BACKGROUND = pyg.image.load('assets/bg.jpg')

clock = pyg.time.Clock()

# initial rectangle position (top left corner)
x = GRID_TLC_x + GRID_ELEM_SIZE * int(GRID_NR_OF_ROWS/2)
y = GRID_TLC_y

one_second_passed = True
ms_count = 0
ms_count_prev = 0

game_running = True    
while game_running:
    # pressing the "X" button terminates the application
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            game_running = False
            
    update_tile_position()
    update_scene()
    
    # limits game's fps (waits) and returns the ms count since the last call
    clock.tick(FPS)
            
pyg.quit()