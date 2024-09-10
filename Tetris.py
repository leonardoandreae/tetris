import pygame as pyg
import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))
import GameParameters as par
import Tile
import numpy as np

def event_handler(tile):
    global game_running, fall_ev

    for event in pyg.event.get():
        # pressing the "X" button terminates the application
        if event.type == pyg.QUIT:
            game_running = False
        if event.type == fall_ev:
            tile.is_falling = True
        
            
def draw_grid():
    for column in range(par.GRID_TLC_y, par.GRID_TLC_y + par.GRID_ELEM_SIZE * par.GRID_NR_OF_COLS, par.GRID_ELEM_SIZE):
        for row in range(par.GRID_TLC_x, par.GRID_TLC_x + par.GRID_ELEM_SIZE * par.GRID_NR_OF_ROWS, par.GRID_ELEM_SIZE):
            # create rectangle object
            grid_element = pyg.Rect(column, row, par.GRID_ELEM_SIZE, par.GRID_ELEM_SIZE)
            pyg.draw.rect(game_window, par.BLACK, grid_element, 1)
            
            
def collision_detection():
    collision_detected = False
    return collision_detected


def update_scene(tile_pos, tile_config_mat):
    # color background such that older objects do not appear
    game_window.blit(BACKGROUND, par.BACKGROUND_POS)
    game_window.blit(tetris_logo, par.LOGO_POS)
    
    draw_grid()
    
    # draw tile
    for col in range (0,4):
        for row in range (0,4):
           if tile_config_mat[col][row] == 1:
               tile_element = pyg.Rect(tile_pos.x + par.GRID_ELEM_SIZE * col, tile_pos.y + par.GRID_ELEM_SIZE * row, par.GRID_ELEM_SIZE, par.GRID_ELEM_SIZE)
               pyg.draw.rect(game_window, par.RED, tile_element)
                
    # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
    pyg.display.update()
    
def get_user_inputs():
    keys_pressed = pyg.key.get_pressed()
    return keys_pressed

def main():
    global game_window, BACKGROUND, tetris_logo, game_running, fall_ev
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
    
    # detect if tile needs to fall by one square
    fall_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
    pyg.time.set_timer(fall_ev, par.FALL_TIME_INTERVAL_ms)
    
    tile = Tile.Tile("L")
    lateral_key_released = True
    rotation_key_released = True

    game_running = True    
    while game_running:
        event_handler(tile)
        [lateral_key_released, rotation_key_released] = tile.update_position(lateral_key_released, rotation_key_released)
        update_scene(tile.position, tile.configuration_matrix)
        
        # limits game's fps (waits) and returns the ms count since the last call
        clock.tick(par.FPS)          
    pyg.quit() 
    
if __name__ == "__main__":
    main()