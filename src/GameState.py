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
        self.lines = 0
        self.score = 0
        self.level = 1
        
    def get_current_keys(self) -> None:
        self.keys_pressed = pyg.key.get_pressed()
    
    def lateral_movement_check(self):
        if self.lateral_movement_disabled and \
                ((not self.keys_pressed[par.LEFT]) and (not self.keys_pressed[par.RIGHT])):
            self.lateral_movement_disabled = False
        
    def rotation_check(self):
        if self.rotation_disabled and (not self.keys_pressed[par.ROTATE]):
            self.rotation_disabled = False

    def rotation_allowed_check(self, tile):
        # TODO refactor this as a recursive function
        # Attempt to rotate the tile and check if there's overlap or out of bounds outcomes
        initial_position = tile.position.x
        tile.rotate('CCW')
        if (not tile.is_overlapping(self)) and (not tile.is_out_of_bounds(self)):
            tile.rotation_allowed = True
        else:
            # Kick tile to the right
            if tile.position.x < par.GRID_TLC_x + par.GRID_ELEM_SIZE * (par.GRID_NR_OF_COLS - 1):
                tile.position.x += 1
                if (not tile.is_overlapping(self)) and (not tile.is_out_of_bounds(self)):
                    tile.rotation_allowed = True
                else:
                    # Kick tile to the left 
                    tile.position.x = initial_position
                    if tile.position > par.GRID_TLC_x:
                        tile.position.x -= 1
                        if (not tile.is_overlapping(self)) and (not tile.is_out_of_bounds(self)):
                            tile.rotation_allowed = True
        # Undo rotation and shift if rotation not allowed
        if tile.rotation_allowed == False:
            tile.rotate('CW')
            tile.position.x = initial_position
       
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
        # TODO add collision detection in the top direction

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
    
    def compute_drop_distance(self, row_start, row_end):
        distances = []
        for col in range(0, par.GRID_NR_OF_COLS):
            d_up = 1
            d_down = 1
            while(row_start - d_up > row_end):
                if self.board_occupation_matrix[row_start - d_up][col] == None:
                    d_up += 1
                else:
                    break 
            while(row_start + d_down < par.GRID_NR_OF_ROWS):
                if self.board_occupation_matrix[row_start + d_down][col] == None:
                    d_down += 1
                else:
                    break  
            distances.append(d_up + d_down - 1)
        return min(distances)

    def drop_block(self, row_start, row_end):
        if ((row_start == 1) and (row_end == 0)):
            for col in range(0, par.GRID_NR_OF_COLS):
                self.board_occupation_matrix[row_start][col] = self.board_occupation_matrix[row_end][col]
                self.board_occupation_matrix[row_end][col] = None
        else:
            d = self.compute_drop_distance(row_start, row_end)
            for col in range(0, par.GRID_NR_OF_COLS):
                for row in range(row_start, row_end, -1):
                    if row - d < 0:
                        self.board_occupation_matrix[row][col] = None
                    else:
                        self.board_occupation_matrix[row][col] = self.board_occupation_matrix[row - d][col]

    def remove_subsequent_completed_rows(self, row_complete_list):
        reduced_row_list = row_complete_list.copy()
        idx = 0
        delta = 1
        while (idx < len(row_complete_list) - 1):
            while (row_complete_list[idx] - delta == row_complete_list[idx + delta]):
                reduced_row_list.remove(row_complete_list[idx + delta])
                delta += 1
            idx += delta
            delta = 1
        return reduced_row_list

    def delete_complete_rows(self):
        row_complete_list = self.get_complete_rows()
        self.nr_of_completed_rows = len(row_complete_list)
        self.lines += self.nr_of_completed_rows
        if self.nr_of_completed_rows != 0:
            for col in range(0, par.GRID_NR_OF_COLS):
                for row in row_complete_list:
                    self.board_occupation_matrix[row][col] = None
            row_complete_list.append(0) # adding the 0 to call drop_block() on the last row
            # remove subsequent entries to make drop distance computation easier
            reduced_list = self.remove_subsequent_completed_rows(row_complete_list)
            for i in range(len(reduced_list) - 1):
                self.drop_block(reduced_list[i], reduced_list[i + 1])
            
    def game_over_check(self):
        for col in range(0, par.GRID_NR_OF_COLS):
            if self.board_occupation_matrix[0][col] == 1:
                self.game_running = False