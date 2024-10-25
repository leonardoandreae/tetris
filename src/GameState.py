import pygame as pyg
import GameParameters as par
from Tile import *
import numpy as np

class GameState:
    def __init__(self):
        self.game_running = True
        self.board_occupation_matrix = [[None for _ in range(par.GRID_NR_OF_COLS)] 
                                        for _ in range(par.GRID_NR_OF_ROWS)]
        self.get_current_keys()
        self.lateral_movement_disabled = False
        self.rotation_disabled = False
        self.clock = pyg.time.Clock()
        # event to detect if tile needs to fall by one square, triggered at regular time intervals
        self.gravity_tick_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
        pyg.time.set_timer(self.gravity_tick_ev, par.FALL_TIME_INTERVAL_ms) 
        # Collision flags
        self.left_collision = False
        self.right_collision = False
        self.down_collision = False
        
    def get_current_keys(self) -> None:
        self.keys_pressed = pyg.key.get_pressed()
    
    def lateral_movement_check(self):
        if self.lateral_movement_disabled and \
                ((not self.keys_pressed[par.LEFT]) and (not self.keys_pressed[par.RIGHT])):
            self.lateral_movement_disabled = False
        
    def rotation_check(self):
        if self.rotation_disabled and (not self.keys_pressed[par.ROTATE]):
            self.rotation_disabled = False
        
    def update_occupation_matrix(self, tile) -> None:
        for row in range(0, len(tile.configuration_matrix)):
            for col in range(0, len(tile.configuration_matrix)):
                if tile.configuration_matrix[row][col] == 1:
                    row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                    col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    self.board_occupation_matrix[row_][col_] = par.TILE_COLORS[tile.type]

    def collision_detection(self, tile):
        # Check collision on the left
        self.left_collision = False # reset every frame
        for row in range(0, len(tile.configuration_matrix)):
            if self.left_collision == True:
                break
            for col in range(0, len(tile.configuration_matrix)):
                row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                col_left_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col - 1
                if tile.configuration_matrix[row][col] == 1 and \
                        (col_left_ < 0 or \
                        self.board_occupation_matrix[row_][col_left_] != None):
                    self.left_collision = True
                    break

        # Check collision on the right
        self.right_collision = False # reset every frame
        for row in range(0, len(tile.configuration_matrix)):
            if self.right_collision == True:
                break
            for col in range(len(tile.configuration_matrix) - 1, -1, -1):
               row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
               col_right_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col + 1
               if tile.configuration_matrix[row][col] == 1 and \
                        (col_right_ > par.GRID_NR_OF_COLS - 1 or \
                        self.board_occupation_matrix[row_][col_right_] != None):
                    self.right_collision = True
                    break
        
        # Check collision at the bottom
        self.down_collision = False # reset every frame
        for row in range(len(tile.configuration_matrix) - 1, -1, -1):
            if self.down_collision == True:
                break
            for col in range(0, len(tile.configuration_matrix)):
                row_down_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row + 1
                col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                if tile.configuration_matrix[row][col] == 1 and \
                          (row_down_ > par.GRID_NR_OF_ROWS - 1 or \
                        self.board_occupation_matrix[row_down_][col_] != None):
                    self.down_collision = True
                    break

    def get_complete_rows(self):
        col_completion_count = 0
        row_complete_list = []
        for row in range(par.GRID_NR_OF_ROWS - 1, -1, -1): # bottom -> top
            for col in range(0, par.GRID_NR_OF_COLS):
                if self.board_occupation_matrix[row][col] != None:
                    col_completion_count += 1
                else: 
                    col_completion_count = 0
                    break
                if col_completion_count == par.GRID_NR_OF_COLS:
                    row_complete_list.append(row)
                    col_completion_count = 0
        return row_complete_list

    def drop_block(self, row_start, row_end):
        for col in range(0, par.GRID_NR_OF_COLS):
            for row in range(row_start, row_end, -1):
                self.board_occupation_matrix[row][col] = self.board_occupation_matrix[row - 1][col]

    def delete_complete_rows(self):
        row_complete_list = self.get_complete_rows()
        for col in range(0, par.GRID_NR_OF_COLS):
            for row in row_complete_list:
                self.board_occupation_matrix[row][col] = None
        row_complete_list.append(0) # adding the 0 to call drop_block() on the last row
        for i in range(len(row_complete_list) - 1):
            self.drop_block(row_complete_list[i], row_complete_list[i + 1])
            
    def game_over_check(self):
        for col in range(0, par.GRID_NR_OF_COLS):
            if self.board_occupation_matrix[0][col] == 1:
                self.game_running = False


                    
    
    
