import parameters as par
import pygame as pyg
import random
from queue import Queue

class Tile:
    """ Class representing a Tetris tetromino tile.
    
    Attributes
    ----------
    is_falling : bool
        Indicates whether the tile is currently falling due to gravity.
    can_soft_drop : bool
        Indicates whether the tile can perform a soft drop.
    position : pyg.Vector2  
        The current position of the tile on the game board.
        
    """
    
    def __init__(self, game_state) -> None:
        """ Initializes the Tile object.
        
        Parameters
        ----------
        game_state : GameState
            The current game state.

        """

        self._listeners = {}
        # Down contact timer -> used to check how long the tile has been in contact with the ground
        self._down_contact_timer_ms = 0
        # tile queue
        self._tile_queue = Queue(maxsize=par.TILE_QUEUE_SIZE)
        for _ in range(par.TILE_QUEUE_SIZE):
            self._tile_queue.put(Tile.get_random_tile_type())
        self.reset(game_state)


    def reset(self, game_state):
        """ Resets the tile to the next type in the queue and initializes its position and state.
        
        Parameters
        ----------
        game_state : GameState
            The current game state.

        """

        self._type = self._tile_queue.queue[0]
        self._next_type = self._tile_queue.queue[1]
        self._rotation_allowed = False
        self._configuration_idx = 0
        self._configuration_matrix = par.TILE_SHAPES[self._type][self._configuration_idx]

        self.is_falling = False
        self.can_soft_drop = False
        self.position = self.get_initial_position()
        
        # Check for contact and if occurred end the game
        game_state.contact_detection(self)
        if game_state.get_contact_flags("down"):
            game_state.game_running = False


    def on(self, event, callback):
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


    def emit(self, event, data = None):
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


    @staticmethod
    def get_random_tile_type() -> str:
        """ Returns a random tile type from the available tile shapes.
        
        """

        tile_types = list(par.TILE_SHAPES.keys())
        idx = random.randint(0, len(tile_types) - 1)
        return tile_types[idx]
    

    def get_current_type(self) -> str:
        """ Returns the current tile type.
        
        """

        return self._type
    

    def get_next_type(self) -> str:
        """ Returns the next tile type in the queue.
        
        """

        return self._next_type
    

    def get_cfg_matrix(self) -> list:
        """ Returns the current configuration matrix of the tile.
        
        """

        return self._configuration_matrix
    
    
    def rotate(self, direction) -> None:
        """ Rotates the tile in the specified direction.
        
        Parameters
        ----------
        direction : str
            The direction to rotate the tile ('CW' for clockwise, 'CCW' for counter-clockwise).
        """

        if direction == 'CCW':
            self._configuration_idx = (self._configuration_idx + 1) % par.TILE_CONFIG_IDX_MAX
        elif direction == 'CW':
            self._configuration_idx = (self._configuration_idx - 1) % par.TILE_CONFIG_IDX_MAX
        else:
            pass
        self._configuration_matrix = par.TILE_SHAPES[self._type][self._configuration_idx]


    def get_initial_position(self) -> pyg.Vector2:
        """ Returns the initial position of the tile based on its type.

        """

        if self._type == "I" or self._type == "O":
            pos = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * (int(par.GRID_NR_OF_COLS / 2) - 2),
                                    par.GRID_TLC_y - par.GRID_ELEM_SIZE)
        else:
            pos = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * (int(par.GRID_NR_OF_COLS / 2) - 1),
                                    par.GRID_TLC_y - par.GRID_ELEM_SIZE)
        return pos


    def is_out_of_bounds(self, x, y) -> bool:
        """ Checks if the given (x, y) position is out of the game board bounds.

        Parameters
        ----------
        x : int
            The x coordinate to check.
        y : int
            The y coordinate to check.

        """

        if (x < par.GRID_TLC_x or \
                x > par.GRID_TLC_x + (par.GRID_NR_OF_COLS - 1) * par.GRID_ELEM_SIZE or \
                y < par.GRID_TLC_y or \
                y > par.GRID_TLC_y + (par.GRID_NR_OF_ROWS - 1) * par.GRID_ELEM_SIZE):
            return True
        else:
            return False


    def compute_smallest_drop_distance(self, game_state) -> int:
        """ Computes the smallest distance (number of cells) that the tile can drop until it hits another tile
        or the bottom of the board.

        Parameters
        ----------
        game_state: GameState
            The current game state.

        """
         
        drop_distances = []
        for col in range(0, par.TILE_CONFIG_IDX_MAX):
            d = 0
            for row in range(par.TILE_CONFIG_IDX_MAX - 1, -1, -1):
                if self._configuration_matrix[row][col] == 1:
                    row_ = int((self.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                    col_ = int((self.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    while(row_ + 1 < par.GRID_NR_OF_ROWS):
                        if game_state.get_BOM_element(row_ + 1, col_) == None:
                            d += 1
                            row_ += 1
                        else:
                            break
                    drop_distances.append(d)
        return min(drop_distances)


    def is_position_permitted(self, game_state) -> bool:
        """ Checks if the current tile position is permitted (i.e., within bounds and not overlapping with the board).
        
        Parameters
        ----------
        game_state : GameState
            The current game state.
        """

        for row in range(0, len(self._configuration_matrix)):
            for col in range(0, len(self._configuration_matrix)):
                # Check if the tile block is out of bounds
                block_pos_x = self.position.x + par.GRID_ELEM_SIZE * col
                block_pos_y = self.position.x + par.GRID_ELEM_SIZE * row
                if self._configuration_matrix[row][col] == 1 and self.is_out_of_bounds(block_pos_x, block_pos_y):
                    return False
                elif self._configuration_matrix[row][col] == 1 and (not self.is_out_of_bounds(block_pos_x, block_pos_y)):
                    # Check if the tile block is overlapping the board
                    row_ = int((self.position.y - par.GRID_TLC_y) / par.GRID_ELEM_SIZE) + row
                    col_ = int((self.position.x - par.GRID_TLC_x) / par.GRID_ELEM_SIZE) + col
                    if game_state.get_BOM_element(row_, col_) != None:
                        return False
                else:
                    pass
        return True
    

    def rotation_allowed_check(self, game_state, step) -> bool:
        """ Checks if rotation is allowed following the wall kick rules.
        
        Parameters
        ----------
        game_state : GameState
            The current game state.
        step : int
            The current step in the wall kick check process.

        """

        if step == 1:
            # Attempt rotating and check if new position is ok
            self.rotate('CCW')
        elif step == 2:
            # Translate to the right and try again
            self.position.x += par.GRID_ELEM_SIZE
        elif step == 3:
            # Translate to the left and try again
            self.position.x -= 2 * par.GRID_ELEM_SIZE
        else: 
            pass
        if self.is_position_permitted(game_state):
            self.rotate('CW')
            return True
        else:
            if self._type == "I":
                self.rotate('CW')
                return False
            else:
                if step == 3:
                    # reset position
                    self.position.x += 2 * par.GRID_ELEM_SIZE
                    return False
                else:
                    self.rotation_allowed_check(game_state, step + 1)
                    
                    
    def update_position(self, game_state) -> None:
        """ Update the tile position based on the current game state and user input.

        Parameters
        ----------
        game_state : GameState
            The current game state.
        """

        # Check if lateral movement is disabled/enabled
        game_state.lateral_movement_check()
            
        # Check if rotation is disabled/enabled
        game_state.rotation_check()

        game_state.contact_detection(self)
        
        # Update left
        if (game_state.keys_pressed[par.LEFT] and (not game_state.keys_pressed[par.RIGHT])
                and (not game_state.get_contact_flags("left"))
                and (not game_state.lateral_movement_disabled)):
            self.position.x -= par.GRID_ELEM_SIZE
            game_state.lateral_movement_disabled = True
            
        # Update right
        if (game_state.keys_pressed[par.RIGHT] and (not game_state.keys_pressed[par.LEFT])
                and (not game_state.get_contact_flags("right"))
                and (not game_state.lateral_movement_disabled)):
            self.position.x += par.GRID_ELEM_SIZE
            game_state.lateral_movement_disabled = True
            
        # Update rotation state
        if (game_state.keys_pressed[par.ROTATE] and self.rotation_allowed_check(game_state, step=1) and (not game_state.rotation_disabled)):
            self.rotate('CCW')
            self.emit("rotation")
            game_state.rotation_disabled = True
        
        # Update vertical position
        if (not game_state.get_contact_flags("down")):
            if game_state.keys_pressed[par.DOWN]:
                self.position.y += int(self.can_soft_drop) * par.GRID_ELEM_SIZE
                if self.can_soft_drop:
                    game_state.increase_score("soft_drop")
                self.can_soft_drop = False
            elif game_state.keys_pressed[par.HARD_DROP]:
                drop_dist = self.compute_smallest_drop_distance(game_state)
                self.position.y += drop_dist * par.GRID_ELEM_SIZE
                game_state.increase_score("hard_drop", drop_distance=drop_dist)
            else: # else needed here to avoid dropping twice due to pressing DOWN and gravity tick
                if (self.is_falling):
                    self.position.y += par.GRID_ELEM_SIZE
                    self.is_falling = False                
        else:
            if (self._down_contact_timer_ms >= par.DOWN_CONTACT_TIMEOUT_ms):
                self._down_contact_timer_ms = 0
                game_state.update_occupancy_matrix(self)
                # remove current tile from the queue...
                self._tile_queue.get()
                # ...and add a new one
                self._tile_queue.put(Tile.get_random_tile_type())
                self.reset(game_state) 
            self._down_contact_timer_ms += game_state.get_clock().get_time()           