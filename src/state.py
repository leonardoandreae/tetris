import pygame as pyg
import parameters as par
from tile import *
from queue import Queue
import random

class GameState:
    def __init__(self, play_sfx):
        self.play_sfx = play_sfx
        self.game_running = True
        self.board_occupation_matrix = [[None for _ in range(par.GRID_NR_OF_COLS)] 
                                        for _ in range(par.GRID_NR_OF_ROWS)]
        self.get_current_keys()
        self.lateral_movement_disabled = False
        self.rotation_disabled = False
        self.clock = pyg.time.Clock()
        # event to detect if tile needs to fall by one square, triggered at regular time intervals
        self.gravity_tick_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
        self.downwards_drop_ev = pyg.USEREVENT + 1
        pyg.time.set_timer(self.gravity_tick_ev, par.FALL_TIME_INTERVAL_ms) 
        pyg.time.set_timer(self.downwards_drop_ev, par.DROP_TIME_INTERVAL_ms)
        # Contact flags
        self.left_contact = False
        self.right_contact = False
        self.down_contact = False
        self.lines = 0
        self.score = 0
        self.level = 1
        # tile queue
        self.tile_queue = Queue(maxsize=par.TILE_QUEUE_SIZE)
        for _ in range(par.TILE_QUEUE_SIZE):
            self.tile_queue.put(self.get_random_tile_type())

    def get_random_tile_type(self):
        tile_types = list(par.TILE_SHAPES.keys())
        idx = random.randint(0, len(tile_types) - 1)
        return tile_types[idx]
   
    def get_current_keys(self) -> None:
        self.keys_pressed = pyg.key.get_pressed()
    
    def lateral_movement_check(self):
        if self.lateral_movement_disabled and \
                ((not self.keys_pressed[par.LEFT]) and (not self.keys_pressed[par.RIGHT])):
            self.lateral_movement_disabled = False
        
    def rotation_check(self):
        if self.rotation_disabled and (not self.keys_pressed[par.ROTATE]):
            self.rotation_disabled = False

    def rotation_allowed_check(self, tile, step):
        if step == 1:
            # Attempt rotating and check if new position is ok
            tile.rotate('CCW')
        elif step == 2:
            # Translate to the right and try again
            tile.position.x += par.GRID_ELEM_SIZE
        elif step == 3:
            # Translate to the left and try again
            tile.position.x -= 2 * par.GRID_ELEM_SIZE
        else: 
            pass
        if tile.is_position_permitted(self):
            tile.rotate('CW')
            return True
        else:
            if tile.type == "I":
                tile.rotate('CW')
                return False
            else:
                if step == 3:
                    # reset position
                    tile.position.x += 2 * par.GRID_ELEM_SIZE
                    return False
                else:
                    self.rotation_allowed_check(tile, step + 1)
            
    def update_occupation_matrix(self, tile) -> None:
        for row in range(0, len(tile.configuration_matrix)):
            for col in range(0, len(tile.configuration_matrix)):
                if tile.configuration_matrix[row][col] == 1:
                    row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                    col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    self.board_occupation_matrix[row_][col_] = par.TILE_COLORS[tile.type]

    def contact_detection(self, tile):
        # Check contact on the left
        self.left_contact = False # reset every frame
        for row in range(0, len(tile.configuration_matrix)):
            if self.left_contact == True:
                break
            for col in range(0, len(tile.configuration_matrix)):
                row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                col_left_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col - 1
                if tile.configuration_matrix[row][col] == 1 and \
                        (col_left_ < 0 or \
                        self.board_occupation_matrix[row_][col_left_] != None):
                    self.left_contact = True
                    break

        # Check contact on the right
        self.right_contact = False # reset every frame
        for row in range(0, len(tile.configuration_matrix)):
            if self.right_contact == True:
                break
            for col in range(len(tile.configuration_matrix) - 1, -1, -1):
               row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
               col_right_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col + 1
               if tile.configuration_matrix[row][col] == 1 and \
                        (col_right_ > par.GRID_NR_OF_COLS - 1 or \
                        self.board_occupation_matrix[row_][col_right_] != None):
                    self.right_contact = True
                    break
        
        # Check contact at the bottom
        self.down_contact = False # reset every frame
        for row in range(len(tile.configuration_matrix) - 1, -1, -1):
            if self.down_contact == True:
                break
            for col in range(0, len(tile.configuration_matrix)):
                row_down_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row + 1
                col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                if tile.configuration_matrix[row][col] == 1 and \
                          (row_down_ > par.GRID_NR_OF_ROWS - 1 or \
                        self.board_occupation_matrix[row_down_][col_] != None):
                    self.down_contact = True
                    break
        # TODO add contact detection in the top direction

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
    
    def increase_score(self, nr_of_completed_rows):
        if nr_of_completed_rows == 1:
            self.score += 40 * self.level
            self.play_sfx("single")
        elif nr_of_completed_rows == 2:
            self.score += 100 * self.level
            self.play_sfx("double")
        elif nr_of_completed_rows == 3:
            self.score += 300 * self.level
            self.play_sfx("triple")
        elif nr_of_completed_rows >= 4:
            self.score += 1200 * self.level
            self.play_sfx("quadruple")
        else:
            pass

    def increase_level(self):
        if self.level < 10:
            self.level += 1
            # speed up tile descent
            par.FALL_TIME_INTERVAL_ms -= par.FALL_TIME_INTERVAL_DELTA_ms
            pyg.time.set_timer(self.gravity_tick_ev, par.FALL_TIME_INTERVAL_ms) # reset timer

    def delete_complete_rows(self):
        lines_prev = self.lines
        row_complete_list = self.get_complete_rows()
        self.nr_of_completed_rows = len(row_complete_list)
        self.lines += self.nr_of_completed_rows
        if (self.lines % 10) < (lines_prev % 10):
           self.increase_level()
        self.increase_score(self.nr_of_completed_rows)
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