import pygame as pyg
import parameters as par
from tile import *
from state import *
from button import *

class GameInterface:
    """The main interface to the game.

    The class provides access to the game-loop functions as well as the necessary 
    drawing toold needed to render the game window. The class also provides all
    the necessary music and sfx components.

    ...

    Attributes
    ----------
    state : GameState
        Object representing the game state needed to track the status of time varying game elements.
    tile : Tile
        Object representing the currently descending tetromino.

    """

    def __init__(self):
        pyg.init()
        self.game_window = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
        pyg.display.set_caption("Tetris")
        self.icon = pyg.image.load('assets/tetris_icon.png') # https://www.freepik.com/icons/tetris Icon by Freepik
        pyg.display.set_icon(self.icon)
        self.logo = pyg.image.load('assets/tetris_logo.png')
        self.logo = pyg.transform.smoothscale_by(self.logo, par.LOGO_SCALE_FACTOR)
        self.text_font_1 = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_1)
        self.text_font_2 = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_2)
        pyg.mixer.music.load('assets/tetris-theme.mp3')
        self.rotation_sfx = pyg.mixer.Sound('assets/rotation.mp3')
        self.single_sfx = pyg.mixer.Sound('assets/single.mp3')
        self.double_sfx = pyg.mixer.Sound('assets/double.mp3')
        self.triple_sfx = pyg.mixer.Sound('assets/triple.mp3')
        self.tetris_sfx = pyg.mixer.Sound('assets/tetris.mp3')
        self.resume_button = Button(par.RESUME_BUTTON_POS, 'Resume')
        self.transparent_overlay = pyg.Surface((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT), pyg.SRCALPHA)
        self.fall_time_interval_ms = par.INITIAL_FALL_TIME_INTERVAL_ms

        self.pause_info_text_surface, _ = self.text_font_1.render(f'Press "Esc" to pause the game', par.WHITE)
        self.next_piece_text_surface, _ = self.text_font_2.render(f'Next:', par.WHITE)
        self.y_level = par.STATS_POS[1] + self.text_font_1.get_sized_height() + par.STATS_VERTICAL_SPACING
        self.x_level = par.STATS_POS[0]
        self.y_lines = self.y_level + self.text_font_1.get_sized_height() + par.STATS_VERTICAL_SPACING
        self.x_lines = self.x_level

        self.state = GameState()
        self.state.on("lines_completed", self.play_sfx_callback)
        self.state.on("soft_drop", self.play_sfx_callback)
        self.state.on("hard_drop", self.play_sfx_callback)
        self.state.on("rotation", self.play_sfx_callback)
        self.state.on("game_paused", self.paused_state_callback)
        self.state.on("game_resumed", self.paused_state_callback)
        self.state.on("level_up", self.level_up_callback)

        # event to detect if tile needs to fall by one square due to gravity, triggered at regular time intervals
        self.gravity_tick_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
        # event to detect if tile can soft drop, triggered at regular time intervals
        self.soft_drop_ev = pyg.USEREVENT + 1
        pyg.time.set_timer(self.gravity_tick_ev, self.fall_time_interval_ms) 
        pyg.time.set_timer(self.soft_drop_ev, par.SOFT_DROP_TIME_INTERVAL_ms)

        self.tile = Tile(self.state)
        self.tile.on("rotation", self.play_sfx_callback)

        self.play_main_theme()
        
    def process_events_and_inputs(self):
        """Calls the event handler and retrieves the user's inputs.

        """

        self.event_handler()
        self.state.get_current_keys()


    def update(self):
        self.state.update_pause_state(self.resume_button.is_activated())
        if not self.state.is_game_paused():  
            self.tile.update_position(self.state)
            self.state.delete_completed_rows()
            self.state.game_over_check()

    def event_handler(self):
        for event in pyg.event.get():
            # pressing the "X" button terminates the application
            if event.type == pyg.QUIT:
                self.state.game_running = False
            if event.type == self.gravity_tick_ev:
                self.tile.is_falling = True
            if event.type == self.soft_drop_ev:
                self.tile.can_soft_drop = True
            if event.type == pyg.KEYUP and event.key == par.PAUSE:
                self.state.pause_key_released = True


    def play_sfx_callback(self, event, data = None):
        if event == "rotation":
            self.play_sfx("rotation")
        elif event == "lines_completed":
            sfx_map = {
                1: "single",
                2: "double",
                3: "triple",
                4: "tetris"
            }
            if data in sfx_map:
                self.play_sfx(sfx_map[data])
        elif event == "soft_drop":
            pass  # TODO: add soft drop sfx
        elif event == "hard_drop":
            pass  # TODO: add hard drop sfx
        else:
            pass


    def paused_state_callback(self, event, data = None):
        if event == "game_paused":
            # Pause gravity
            pyg.time.set_timer(self.gravity_tick_ev, 0)
            # Pause music
            pyg.mixer.music.pause()
        elif event == "game_resumed":
            # Resume gravity
            pyg.time.set_timer(self.gravity_tick_ev, self.fall_time_interval_ms)
            # Resume music
            pyg.mixer.music.unpause()
        else:
            pass


    def level_up_callback(self, event, data = None):
        if event == "level_up":
            # speed up tile descent
            self.fall_time_interval_ms -= par.FALL_TIME_INTERVAL_DELTA_ms
            pyg.time.set_timer(self.gravity_tick_ev, self.fall_time_interval_ms)
        else:
            pass


    def play_sfx(self, sfx_type):
        if sfx_type == "rotation":
            self.rotation_sfx.play()
        elif sfx_type == "single":
            self.single_sfx.play()
        elif sfx_type == "double":
            self.double_sfx.play()
        elif sfx_type == "triple":
            self.triple_sfx.play()
        elif sfx_type == "tetris":
            self.tetris_sfx.play()
        elif sfx_type == "soft_drop":
            pass  # TODO: add soft drop sfx
        elif sfx_type == "hard_drop":
            pass  # TODO: add hard drop sfx
        else:
            pass
        

    def play_main_theme(self):
        pyg.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
        pyg.mixer.music.set_volume(par.MUSIC_VOLUME)

    def draw_grid(self, nr_of_rows, nr_of_cols, TLC_coords, color=par.DEFAULT_GRID_COLOR):
        """Draws a grid at the specified position with the specified dimensions.

        Parameters
        ----------
        nr_of_rows: int
            Number of rows of the grid.
        nr_of_cols: int
            Numer of columns of the grid.
        TLC_coords: pygame.Vector2
            Coordinates of the top left corner of the grid.
        """

        # draw horizontal lines
        for row_idx in range(0, nr_of_rows + 1):
            start_coords = (TLC_coords.x, TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            end_coords = (TLC_coords.x + nr_of_cols * par.GRID_ELEM_SIZE, 
                        TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            pyg.draw.line(surface=self.game_window, color=color, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)
        # draw vertical lines    
        for col_idx in range(0, nr_of_cols + 1):
            start_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, TLC_coords.y)
            end_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, 
                         TLC_coords.y + par.GRID_ELEM_SIZE * nr_of_rows)
            pyg.draw.line(surface=self.game_window, color=color, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)

    def draw_block_with_borders(self, TLC_x, TLC_y, size, color, border_color):
        block = pyg.Rect(TLC_x, TLC_y, size, size)
        pyg.draw.rect(self.game_window, color, block)
        top_left = (TLC_x, TLC_y) 
        down_left = (top_left[0], top_left[1] + size)
        down_right = (down_left[0] + size, down_left[1])
        top_right = (down_right[0], down_right[1] - size)
        pyg.draw.lines(surface=self.game_window, color=border_color, closed=True,
                    points=[top_left, down_left, down_right, top_right],
                    width=par.BLOCK_BORDER_THICKNESS)

    def draw_board(self):
        for row in range (0, par.GRID_NR_OF_ROWS):
            for col in range (0, par.GRID_NR_OF_COLS):
                if self.state.get_BOM_element(row, col) != None:
                    self.draw_block_with_borders(par.GRID_TLC_x + col * par.GRID_ELEM_SIZE,
                                                 par.GRID_TLC_y + row * par.GRID_ELEM_SIZE,
                                                 par.GRID_ELEM_SIZE,
                                                 self.state.get_BOM_element(row, col),
                                                 par.WHITE)

    def draw_tile(self, tile_type, cfg_mat, pos_x, pos_y, border_color = par.WHITE):
        # draw tile with its border
        for col in range (0, par.TILE_CONFIG_IDX_MAX):
            for row in range (0, par.TILE_CONFIG_IDX_MAX):
                if cfg_mat[row][col] == 1:
                    self.draw_block_with_borders(pos_x + par.GRID_ELEM_SIZE * col,
                                                pos_y + par.GRID_ELEM_SIZE * row,
                                                par.GRID_ELEM_SIZE,
                                                par.TILE_COLORS[tile_type],
                                                border_color)

                    
    def draw_dropped_tile_preview(self, color: tuple = par.WHITE) -> None:
        """ Draws the outline of where the current tile would land if dropped immediately.

        Parameters
        ----------
        color: tuple
            RGB color of the outline.
        """

        drop_distance = self.tile.compute_smallest_drop_distance(self.state)
        # draw tile outer border at drop distance
        for row in range (0, par.TILE_CONFIG_IDX_MAX):
            for col in range (0, par.TILE_CONFIG_IDX_MAX):
                if self.tile._configuration_matrix[row][col] == 1:                  
                    if row == 0 or self.tile._configuration_matrix[row - 1][col] == 0: # lazy OR eval allows to avoid idx overflow (same below)
                        pyg.draw.line(self.game_window, 
                                        color, 
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)
                    if col == 0 or self.tile._configuration_matrix[row][col - 1] == 0:
                        pyg.draw.line(self.game_window, 
                                        color, 
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)                            
                    if row == par.TILE_CONFIG_IDX_MAX - 1 or self.tile._configuration_matrix[row + 1][col] == 0:
                        pyg.draw.line(self.game_window, 
                                        color, 
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)  
                    if col == par.TILE_CONFIG_IDX_MAX - 1 or self.tile._configuration_matrix[row][col + 1] == 0:
                        pyg.draw.line(self.game_window, 
                                        color, 
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self.tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)


    def draw_pause_menu(self) -> None:
        """ Draws the pause menu. 
        
        """

        # Draw transparent grey overlay
        pyg.draw.rect(self.transparent_overlay, par.TRANSPARENT_GREY, (pyg.Vector2(0,0), pyg.Vector2(par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT)))
        self.game_window.blit(self.transparent_overlay, par.PAUSE_MENU_TRANSPARENT_OVERLAY_POS)
        self.resume_button.draw(self.game_window)
        pyg.display.update()


    def draw_frame(self) -> None:
        """ Draws the current frame.
        
        """

        # TODO: only draw tile and board each time not the entire thing
        # color background such that older tile positions do not appear
        self.game_window.fill(par.BLACK)
        self.game_window.blit(self.logo, par.LOGO_POS)

        score_text_surface, _ = self.text_font_1.render(f'Score:  {self.state.get_score()}', par.WHITE)
        level_text_surface, _ = self.text_font_1.render(f'Level:   {self.state.get_level()}', par.WHITE)
        lines_text_surface, _ = self.text_font_1.render(f'Lines:   {self.state.get_lines()}', par.WHITE)


        self.game_window.blit(score_text_surface, par.STATS_POS)
        self.game_window.blit(level_text_surface, (self.x_level, self.y_level))
        self.game_window.blit(lines_text_surface, (self.x_lines, self.y_lines))
        self.game_window.blit(self.next_piece_text_surface, par.NEXT_PIECE_TEXT_POS)

        self.game_window.blit(self.pause_info_text_surface, par.PAUSE_INFO_TEXT_POS)
        
        # draw next piece preview grid
        self.draw_grid(par.TILE_CONFIG_IDX_MAX, par.TILE_CONFIG_IDX_MAX, par.NEXT_PIECE_GRID_POS, par.GREY)
        # draw board grid
        self.draw_grid(par.GRID_NR_OF_ROWS, par.GRID_NR_OF_COLS, pyg.Vector2(par.GRID_TLC_x, par.GRID_TLC_y), par.GREY)
        self.draw_board()
        self.draw_tile(self.tile.get_current_type(), 
                       self.tile._configuration_matrix,
                       self.tile.position.x,
                       self.tile.position.y)
        # draw next tile preview
        self.draw_tile(self.tile.get_next_type(),
                       par.TILE_SHAPES[self.tile.get_next_type()][0],
                       par.NEXT_PIECE_GRID_POS.x,
                       par.NEXT_PIECE_GRID_POS.y)
        self.draw_dropped_tile_preview()

        if self.state.is_game_paused():
            self.draw_pause_menu()
        '''
        After calling the drawing functions to make the display Surface object look the way you want
        you must call update() to make the display Surface actually appear on the user’s monitor.
        '''
        if not self.state.is_game_paused():
            pyg.display.update()