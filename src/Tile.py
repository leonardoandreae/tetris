import GameParameters as par
import pygame as pyg
import random

class Tile:
    def __init__(self, game_state) -> None:
        self.reset(game_state)

    def reset(self, game_state):
        self.type = self.get_next_type()
        self.vertical_movement_allowed = True
        self.lateral_movement_allowed = True
        self.rotation_allowed = True
        self.is_falling = False
        self.configuration_idx = 0
        self.position = self.get_initial_position()
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
        # Check for collisions and if occurred end the game
        game_state.collision_detection(self)
        if game_state.down_collision == True:
            game_state.game_running = False


    def get_next_type(self):
        tile_types = list(par.TILE_SHAPES.keys())
        idx = random.randint(0, len(tile_types) - 1)
        return tile_types[idx]
    
    def rotate(self) -> None:
        self.configuration_idx = (self.configuration_idx + 1) % par.TILE_CONFIG_IDX_MAX
        self.configuration_matrix = par.TILE_SHAPES[self.type][self.configuration_idx]
        
    def get_initial_position(self):
        if self.type == "I" or self.type == "O":
            pos = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * (int(par.GRID_NR_OF_COLS / 2) - 2),
                                    par.GRID_TLC_y - par.GRID_ELEM_SIZE)
        else:
            pos = pyg.Vector2(par.GRID_TLC_x + par.GRID_ELEM_SIZE * (int(par.GRID_NR_OF_COLS / 2) - 1),
                                    par.GRID_TLC_y - par.GRID_ELEM_SIZE)
        return pos
        
    def update_position(self, game_state):
        # Check if lateral movement is disabled/enabled
        game_state.lateral_movement_check()
            
        # Check if rotation is disabled/enabled
        game_state.rotation_check()

        game_state.collision_detection(self)
        
        # Update left
        if (game_state.keys_pressed[par.LEFT] and (not game_state.keys_pressed[par.RIGHT])
                and (not game_state.left_collision)
                and (not game_state.lateral_movement_disabled)):
            self.position.x -= par.GRID_ELEM_SIZE
            game_state.lateral_movement_disabled = True
            
        # Update right
        if (game_state.keys_pressed[par.RIGHT] and (not game_state.keys_pressed[par.LEFT])
                and (not game_state.right_collision)
                and (not game_state.lateral_movement_disabled)):
            self.position.x += par.GRID_ELEM_SIZE
            game_state.lateral_movement_disabled = True
            
        # Update rotation state
        if (game_state.keys_pressed[par.ROTATE] and self.rotation_allowed and (not game_state.rotation_disabled)):
            self.rotate()
            game_state.rotation_disabled = True
        
        # Update vertical position
        if (not game_state.down_collision):
            if (self.is_falling):
                self.position.y += par.GRID_ELEM_SIZE
                self.is_falling = False
        else:
            game_state.update_occupation_matrix(self)
            self.reset(game_state)
              