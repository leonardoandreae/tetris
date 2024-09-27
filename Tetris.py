import pygame as pyg
import sys, os
sys.path.append(os.path.join(sys.path[0], 'src'))
import GameParameters as par
from Tile import *
from GameState import *
import numpy as np

def event_handler(tile, game_state):
    for event in pyg.event.get():
        # pressing the "X" button terminates the application
        if event.type == pyg.QUIT:
            game_state.game_running = False
        if event.type == game_state.gravity_tick_ev:
            if not tile.bottom_reached():
                tile.is_falling = True
        
            
def draw_grid():
    for column in range(par.GRID_TLC_y, par.GRID_TLC_y + par.GRID_ELEM_SIZE * par.GRID_NR_OF_COLS, par.GRID_ELEM_SIZE):
        for row in range(par.GRID_TLC_x, par.GRID_TLC_x + par.GRID_ELEM_SIZE * par.GRID_NR_OF_ROWS, par.GRID_ELEM_SIZE):
            # create rectangle object
            grid_element = pyg.Rect(column, row, par.GRID_ELEM_SIZE, par.GRID_ELEM_SIZE)
            pyg.draw.rect(game_window, par.BLACK, grid_element, 1)
            

def update_scene(tile_type, tile_pos, tile_config_mat):
    # TODO: only draw tile each time not the entire thing
    # color background such that older objects do not appear
    game_window.blit(bg, par.BACKGROUND_POS)
    game_window.blit(tetris_logo, par.LOGO_POS)
    
    draw_grid()
    
    # draw tile
    for col in range (0,par.TILE_CONFIG_IDX_MAX):
        for row in range (0,par.TILE_CONFIG_IDX_MAX):
           if tile_config_mat[row][col] == 1:
               tile_element = pyg.Rect(tile_pos.x + par.GRID_ELEM_SIZE * col, tile_pos.y + par.GRID_ELEM_SIZE * row, par.GRID_ELEM_SIZE, par.GRID_ELEM_SIZE)
               pyg.draw.rect(game_window, par.TILE_COLORS[tile_type], tile_element)
                
    # After calling the drawing functions to make the display Surface object look the way you want, you must call this to make the display Surface actually appear on the user’s monitor.
    pyg.display.update()
    
def get_user_inputs():
    keys_pressed = pyg.key.get_pressed()
    return keys_pressed

def main():
    global game_window, bg, tetris_logo
    pyg.init()
    game_window = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
    pyg.display.set_caption("Tetris")
    
    # https://www.freepik.com/icons/tetris Icon by Freepik
    tetris_icon = pyg.image.load('assets/tetris_icon.png')
    pyg.display.set_icon(tetris_icon)

    bg = pyg.image.load('assets/bg.jpg')
    tetris_logo = pyg.image.load('assets/tetris_logo.png')
    tetris_logo = pyg.transform.scale2x(tetris_logo)
    
    game_state = GameState()
    tile = Tile("J")
  
    while game_state.game_running:
        event_handler(tile, game_state)
        
        game_state.get_current_keys()
        tile.update_position(game_state)
        update_scene(tile.type, tile.position, tile.configuration_matrix)
        
        # limits game's fps (waits) and returns the ms count since the last call
        game_state.clock.tick(par.FPS)          
    pyg.quit() 
    
if __name__ == "__main__":
    main()