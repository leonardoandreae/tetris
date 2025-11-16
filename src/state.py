import pygame as pyg
import parameters as par
from tile import *
from queue import Queue
import random

class GameState:
    def __init__(self, play_sfx):
        self.play_sfx = play_sfx
        self.game_running = True
        self.game_paused = False
        self.game_resumed_timer_ms = 0
        self.pause_key_released = False
        self.board_occupancy_matrix = [[None for _ in range(par.GRID_NR_OF_COLS)] 
                                        for _ in range(par.GRID_NR_OF_ROWS)]
        self.get_current_keys()
        self.lateral_movement_disabled = False
        self.rotation_disabled = False
        self.clock = pyg.time.Clock()
        # event to detect if tile needs to fall by one square, triggered at regular time intervals
        self.gravity_tick_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
        self.soft_drop_ev = pyg.USEREVENT + 1
        pyg.time.set_timer(self.gravity_tick_ev, par.FALL_TIME_INTERVAL_ms) 
        pyg.time.set_timer(self.soft_drop_ev, par.SOFT_DROP_TIME_INTERVAL_ms)
        # Contact flags
        self.left_contact = False
        self.right_contact = False
        self.down_contact = False
        # Down contact timer -> used to check how long the tile has been in contact with the ground
        self.down_contact_timer_ms = 0
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
                    self.board_occupancy_matrix[row_][col_] = par.TILE_COLORS[tile.type]

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
                        self.board_occupancy_matrix[row_][col_left_] != None):
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
                        self.board_occupancy_matrix[row_][col_right_] != None):
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
                        self.board_occupancy_matrix[row_down_][col_] != None):
                    self.down_contact = True
                    break

    def get_completed_rows_list(self) -> list:
        """ Returns a list of row indices that are completely filled (i.e., no None values) in the board occupancy matrix.
        
        """
        col_completion_count = 0
        row_complete_list = []
        for row in range(par.GRID_NR_OF_ROWS - 1, -1, -1): # bottom -> top
            for col in range(0, par.GRID_NR_OF_COLS):
                if self.board_occupancy_matrix[row][col] != None:
                    col_completion_count += 1
                else: 
                    col_completion_count = 0
                    break
                if col_completion_count == par.GRID_NR_OF_COLS:
                    row_complete_list.append(row)
                    col_completion_count = 0
        return row_complete_list
   
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

    def delete_completed_rows(self):
        lines_prev = self.lines
        completed_rows_list = self.get_completed_rows_list()
        self.nr_of_completed_rows = len(completed_rows_list)
        self.lines += self.nr_of_completed_rows
        if (self.lines % 10) < (lines_prev % 10): # TODO: rewrite this condition
           self.increase_level()
        self.increase_score(self.nr_of_completed_rows)
        if self.nr_of_completed_rows != 0:
            for col in range(0, par.GRID_NR_OF_COLS):
                for row in completed_rows_list:
                    self.board_occupancy_matrix[row][col] = None
            self.post_deletion_drop(completed_rows_list)


    def drop_block(self, row_start: int, row_end: int, drop_distance: int) -> None:
        """ Drops the blocks above the deleted rows downwards by the specified drop distance.

        Parameters
        ----------
        row_start: int
            The starting (lower) row index (inclusive).
        row_end: int
            The ending (higher) row index (inclusive).
        drop_distance: int
            The distance (in number of cells) to drop the blocks.
        """

        for row in range(row_end + 1, row_start - 1, -1): # in inverse order otherwise it does not work!
            for col in range(0, par.GRID_NR_OF_COLS):
                    if self.board_occupancy_matrix[row][col] != None:
                        self.board_occupancy_matrix[row + drop_distance][col] = self.board_occupancy_matrix[row][col]
                        self.board_occupancy_matrix[row][col] = None


    def post_deletion_drop(self, completed_rows_list: list) -> None:
        """ Drops the blocks above the deleted rows downwards to fill the gaps.

        Parameters
        ----------
        completed_rows_list: list
            A list of row indices that have been completed and deleted (in descending order), non-empty.
        
        """

        idx  = 0
        distance = 1
        while (idx < len(completed_rows_list) and idx + distance < len(completed_rows_list)):
            if (completed_rows_list[idx + distance] == completed_rows_list[idx] - distance):
                distance += 1
            else:
                row_start = completed_rows_list[idx + distance] + 1
                row_end = completed_rows_list[idx] - 1
                self.drop_block(row_start, row_end, distance)
                idx += 1
                distance = 1
        self.drop_block(0, completed_rows_list[-1] - 1, distance)
            

    def game_over_check(self):
        """ Checks if the game is over by verifying if there are any occupied cells in the top row of the board.
        
        """

        for col in range(0, par.GRID_NR_OF_COLS):
            if self.board_occupancy_matrix[0][col] == 1:
                self.game_running = False