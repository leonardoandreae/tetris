import pygame as pyg
import parameters as par
from tile import *


class GameState:
    """ Class representing the game state.

    """

    def __init__(self) -> None:
        """ Initializes the game state.
        
        """

        # ---private attributes---
        self._listeners = {}
        self._game_paused = False
        self._game_resumed_timer_ms = 0
        self._board_occupancy_matrix = [[None for _ in range(par.GRID_NR_OF_COLS)] 
                                        for _ in range(par.GRID_NR_OF_ROWS)]
        self._clock = pyg.time.Clock()
        # Contact flags
        self._left_contact = False
        self._right_contact = False
        self._down_contact = False
        # Game stats
        self._lines = 0
        self._score = 0
        self._level = 1
    
        # ---public attributes---
        self.game_running = True
        self.pause_key_released = False
        self.lateral_movement_disabled = False # to prevent multiple lateral moves on single key press
        self.rotation_disabled = False # to prevent multiple rotations on single key press
        
        
    def on(self, event, callback) -> None:
        """ Subscribe a callback to a named event.

        Parameters
        ----------
        event : str
            The name of the event to listen for.

        callback : function
            The function to call when the event is emitted.

        """

        if event not in self._listeners:
            self._listeners[event] = [] # creates empty list for the event
        self._listeners[event].append(callback)


    def emit(self, event, data = None) -> None:
        """Emit an event and notify listeners.

        Parameters
        ----------
        event : str
            The name of the event to emit.

        data : any, optional
            Additional data to pass to the event listeners.
        """

        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(event, data)
    

    def is_game_paused(self) -> bool:
        """ Returns whether the game is currently paused.
        
        """

        return self._game_paused
    

    def get_BOM_element(self, row: int, col: int) -> tuple:
        """ Returns the board occupancy matrix element at the specified row and column.

        Parameters
        ----------
        row : int
            The row index.
        col : int
            The column index.
        
        """

        return self._board_occupancy_matrix[row][col]
    
    
    def get_clock(self) -> pyg.time.Clock:
        """ Returns the game clock.
        
        """

        return self._clock
    

    def get_contact_flags(self, direction: str) -> bool:
        """ Returns the contact flag for the specified direction.

        Parameters
        ----------
        direction : str
            The direction to check contact for ("left", "right", "down").
        
        """

        if direction == "left":
            return self._left_contact
        elif direction == "right":
            return self._right_contact
        elif direction == "down":
            return self._down_contact
        else:
            raise ValueError("Invalid direction. Must be 'left', 'right', or 'down'.")
        

    def get_lines(self) -> int:
        """ Returns the number of lines cleared.
        
        """

        return self._lines
    

    def get_score(self) -> int:
        """ Returns the current score.
        
        """

        return self._score
    

    def get_level(self) -> int:
        """ Returns the current level.
        
        """

        return self._level


    def get_current_keys(self) -> None:
        """ Updates the current keys pressed state.
        
        """
        self.keys_pressed = pyg.key.get_pressed()
    

    def lateral_movement_check(self) -> None:
        """ Checks if lateral movement keys have been released to re-enable lateral movement.
        
        """

        if self.lateral_movement_disabled and \
                ((not self.keys_pressed[par.LEFT]) and (not self.keys_pressed[par.RIGHT])):
            self.lateral_movement_disabled = False


    def rotation_check(self) -> None:
        """ Checks if rotation key has been released to re-enable rotation.
        
        """

        if self.rotation_disabled and (not self.keys_pressed[par.ROTATE]):
            self.rotation_disabled = False


    def update_occupancy_matrix(self, tile) -> None:
        """ Updates the board occupancy matrix with the current tile's position and configuration.

        Parameters
        ----------
        tile : Tile
            The tile to place on the board.
        """

        for row in range(0, len(tile.configuration_matrix)):
            for col in range(0, len(tile.configuration_matrix)):
                if tile.configuration_matrix[row][col] == 1:
                    row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                    col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    self._board_occupancy_matrix[row_][col_] = par.TILE_COLORS[tile.type]


    def contact_detection(self, tile):
        """ Detects contact of the tile with the board boundaries or occupied cells and updates contact flags.
        
        Parameters
        ----------
        tile : Tile
            The tile to check for contact.
        """

        # Check contact on the left
        self._left_contact = False # reset every frame
        for row in range(0, len(tile.configuration_matrix)):
            if self._left_contact == True:
                break
            for col in range(0, len(tile.configuration_matrix)):
                row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                col_left_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col - 1
                if tile.configuration_matrix[row][col] == 1 and \
                        (col_left_ < 0 or \
                        self._board_occupancy_matrix[row_][col_left_] != None):
                    self._left_contact = True
                    break

        # Check contact on the right
        self._right_contact = False # reset every frame
        for row in range(0, len(tile.configuration_matrix)):
            if self._right_contact == True:
                break
            for col in range(len(tile.configuration_matrix) - 1, -1, -1):
               row_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
               col_right_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col + 1
               if tile.configuration_matrix[row][col] == 1 and \
                        (col_right_ > par.GRID_NR_OF_COLS - 1 or \
                        self._board_occupancy_matrix[row_][col_right_] != None):
                    self._right_contact = True
                    break
        
        # Check contact at the bottom
        self._down_contact = False # reset every frame
        for row in range(len(tile.configuration_matrix) - 1, -1, -1):
            if self._down_contact == True:
                break
            for col in range(0, len(tile.configuration_matrix)):
                row_down_ = int((tile.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row + 1
                col_ = int((tile.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                if tile.configuration_matrix[row][col] == 1 and \
                          (row_down_ > par.GRID_NR_OF_ROWS - 1 or \
                        self._board_occupancy_matrix[row_down_][col_] != None):
                    self._down_contact = True
                    break


    def get_completed_rows_list(self) -> list:
        """ Returns a list of row indices that are completely filled (i.e. no None values) in the board occupancy matrix.
        
        """
        col_completion_count = 0
        row_complete_list = []
        for row in range(par.GRID_NR_OF_ROWS - 1, -1, -1): # bottom -> top
            for col in range(0, par.GRID_NR_OF_COLS):
                if self._board_occupancy_matrix[row][col] != None:
                    col_completion_count += 1
                else: 
                    col_completion_count = 0
                    break
                if col_completion_count == par.GRID_NR_OF_COLS:
                    row_complete_list.append(row)
                    col_completion_count = 0
        return row_complete_list
   

    def increase_score(self, event : str, nr_of_completed_rows : int = None, drop_distance : int = None) -> None:
        """ Increases the score based on the scoring event type and notifies listeners.

        Parameters
        ----------
        event : str
            The type of scoring event.
        nr_of_completed_rows : int, optional
            The number of rows completed (required for "lines_completed" event).
        drop_distance : int, optional
            The drop distance (required for "hard_drop" event).
        
        """

        if event == "lines_completed":
            self._score += par.LINE_CLEAR_SCORE_MULTIPLIERS[nr_of_completed_rows] * self._level
            self.emit(event, nr_of_completed_rows)
        elif event == "soft_drop":
            self._score += 1
            self.emit(event)
        elif event == "hard_drop":
            self._score += par.SCORE_MULTIPLIER_HARD_DROP * drop_distance
            self.emit(event, drop_distance)
        else:
            pass


    def increase_level(self) -> None:
        """ Increases the game level by 1, up to the maximum level, and speeds up the tile descent.
        
        """

        if self._level < par.MAX_LEVEL:
            self._level += 1
            self.emit("level_up")


    def level_up_check(self) -> None:
        """ Checks if the level needs to be increased based on the number of lines cleared.
        
        """

        if self._lines >= self._level * par.MAX_LINES_PER_LEVEL:
            self.increase_level()


    def delete_completed_rows(self) -> None:
        """ Deletes completed rows, updates score and level accordingly, and drops blocks above the deleted rows downwards.
        
        """

        completed_rows_list = self.get_completed_rows_list()
        self._lines += len(completed_rows_list)
        self.level_up_check()

        if len(completed_rows_list) != 0:
            self.increase_score("lines_completed", nr_of_completed_rows=len(completed_rows_list))
            for col in range(0, par.GRID_NR_OF_COLS):
                for row in completed_rows_list:
                    self._board_occupancy_matrix[row][col] = None
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
                    if self._board_occupancy_matrix[row][col] != None:
                        self._board_occupancy_matrix[row + drop_distance][col] = self._board_occupancy_matrix[row][col]
                        self._board_occupancy_matrix[row][col] = None


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


    def update_pause_state(self, resume_button_activated: bool) -> None:
        """ Updates the game pause state and notifies listeners.
        
        Parameters
        ----------
        resume_button_activated: bool
            Indicates if the resume button has been activated."""
        self._game_resumed_timer_ms += self._clock.get_time()
        
        if not self._game_paused and self.keys_pressed[par.PAUSE] and self._game_resumed_timer_ms > par.PAUSE_COOLDOWN_ms:
            self._game_paused = True
            self.pause_key_released = False
            self.emit("game_paused")

        if (self._game_paused and resume_button_activated) or \
           (self._game_paused and self.keys_pressed[par.PAUSE] and self.pause_key_released):
            self._game_resumed_timer_ms = 0
            self._game_paused = False
            self.emit("game_resumed")
            


    def game_over_check(self) -> None:
        """ Checks if the game is over by verifying if there are any occupied cells in the top row of the board.
        
        """

        for col in range(0, par.GRID_NR_OF_COLS):
            if self._board_occupancy_matrix[0][col] == 1:
                self.game_running = False