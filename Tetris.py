import pygame as pyg
import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))
import GameParameters as par

def event_handler():
    global game_running, fall_ev, tile_falling

    for event in pyg.event.get():
        # pressing the "X" button terminates the application
        if event.type == pyg.QUIT:
            game_running = False
        if event.type == fall_ev:
            tile_falling = True
            

def update_tile_position():
    global x, y, ms_count, ms_count_prev, tile_falling, lateral_movement_prevented
    keys_pressed = pyg.key.get_pressed()
    
    if (lateral_movement_prevented == True and (not keys_pressed[pyg.K_LEFT])
            and (not keys_pressed[pyg.K_RIGHT])):
        lateral_movement_prevented = False
                
    
    if (keys_pressed[pyg.K_LEFT] and (not keys_pressed[pyg.K_RIGHT])
            and x > par.GRID_TLC_x and (not lateral_movement_prevented)):
        x -= par.GRID_ELEM_SIZE
        lateral_movement_prevented = True
            
    if (keys_pressed[pyg.K_RIGHT] and (not keys_pressed[pyg.K_LEFT])
            and x < par.GRID_TLC_x + par.GRID_ELEM_SIZE * (par.GRID_NR_OF_COLS - 1)
            and (not lateral_movement_prevented)):
        x += par.GRID_ELEM_SIZE
        lateral_movement_prevented = True
        
    if tile_falling and y < par.GRID_TLC_y + par.GRID_ELEM_SIZE * (par.GRID_NR_OF_ROWS - 1):
        y += par.GRID_ELEM_SIZE
        tile_falling = False
        
            
def draw_grid():
    for column in range(par.GRID_TLC_y, par.GRID_TLC_y + par.GRID_ELEM_SIZE * par.GRID_NR_OF_COLS, par.GRID_ELEM_SIZE):
        for row in range(par.GRID_TLC_x, par.GRID_TLC_x + par.GRID_ELEM_SIZE * par.GRID_NR_OF_ROWS, par.GRID_ELEM_SIZE):
            # create rectangle object
            grid_element = pyg.Rect(column, row, par.GRID_ELEM_SIZE, par.GRID_ELEM_SIZE)
            pyg.draw.rect(game_window, par.BLACK, grid_element, 1)
            
            
def collision_detection():
    collision_detected = False
    return collision_detected


def update_scene():
    # color background such that older objects do not appear
    game_window.blit(BACKGROUND, par.BACKGROUND_POS)
    game_window.blit(tetris_logo, par.LOGO_POS)
    
    draw_grid()
    
    # draw tile
    tile = pyg.Rect(x, y, par.GRID_ELEM_SIZE, par.GRID_ELEM_SIZE)
    pyg.draw.rect(game_window, par.RED, tile)
    # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
    pyg.display.update()

def main():
    global game_window, BACKGROUND, tetris_logo, x, y, game_running, fall_ev, tile_falling, lateral_movement_prevented
    pyg.init()
    game_window = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
    pyg.display.set_caption("Tetris")
    
    # https://www.freepik.com/icons/tetris Icon by Freepik
    tetris_icon = pyg.image.load('assets/tetris_icon.png')
    pyg.display.set_icon(tetris_icon)

    BACKGROUND = pyg.image.load('assets/bg.jpg')
    tetris_logo = pyg.image.load('assets/tetris_logo.png')
    tetris_logo = pyg.transform.scale2x(tetris_logo)
    
    clock = pyg.time.Clock()

    # initial rectangle position (top left corner)
    x = par.GRID_TLC_x + par.GRID_ELEM_SIZE * int(par.GRID_NR_OF_COLS/2)
    y = par.GRID_TLC_y
    
    # detect if tile needs to fall by one square
    fall_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
    pyg.time.set_timer(fall_ev, par.FALL_TIME_INTERVAL_ms)
    tile_falling = False
    lateral_movement_prevented = False

    game_running = True    
    while game_running:
        event_handler()
        update_tile_position()
        update_scene()
        
        # limits game's fps (waits) and returns the ms count since the last call
        clock.tick(par.FPS)          
    pyg.quit() 
    
if __name__ == "__main__":
    main()