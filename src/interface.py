import pygame as pyg
import parameters as par
from tile import *
from state import *
from button import *

class GameInterface:
    """The main interface to the game.

    The class provides access to the game-loop functions as well as the necessary 
    drawing toolbox needed to render the game window. The class also loads all
    the necessary music, sfx and UI components.

    Attributes
    ----------
    state: GameState
        The current state of the game.

    """

    def __init__(self) -> None:
        """ Initializes the game interface.
        
        """
        
        pyg.init() # initialize pygame modules
        
        # set up the game window
        self.game_window_ = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
        pyg.display.set_caption("Tetris")
        
        # load and set the game icon
        self.icon_ = pyg.image.load('assets/tetris_icon.png') # https://www.freepik.com/icons/tetris Icon by Freepik
        pyg.display.set_icon(self.icon_)
        
        # load and scale logo
        self.logo_ = pyg.image.load('assets/tetris_logo.png')
        self.logo_ = pyg.transform.smoothscale_by(self.logo_, par.LOGO_SCALE_FACTOR)
        
        # set up fonts
        self.text_font_1_ = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_1)
        self.text_font_2_ = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_2)
        
        # set up music and sfx
        pyg.mixer.music.load('assets/tetris-theme.mp3')
        self.rotation_sfx_ = pyg.mixer.Sound('assets/rotation.mp3')
        self.single_sfx_ = pyg.mixer.Sound('assets/single.mp3')
        self.double_sfx_ = pyg.mixer.Sound('assets/double.mp3')
        self.triple_sfx_ = pyg.mixer.Sound('assets/triple.mp3')
        self.tetris_sfx_ = pyg.mixer.Sound('assets/tetris.mp3')
        
        # initialize fall time interval
        self.fall_time_interval_ms_ = par.INITIAL_FALL_TIME_INTERVAL_ms
        
        # set up time invariant surfaces
        self.transparent_overlay_ = pyg.Surface((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT), pyg.SRCALPHA)
        self.pause_info_text_surface_, _ = self.text_font_1_.render(f'Press "Esc" to pause the game', par.WHITE)
        self.next_piece_text_surface_, _ = self.text_font_2_.render(f'Next:', par.WHITE)
        
        # precompute text positions
        self.level_text_pos_ = (par.STATS_POS[0], \
            par.STATS_POS[1] + self.text_font_1_.get_sized_height() + par.STATS_VERTICAL_SPACING)
        self.lines_text_pos_ = (self.level_text_pos_[0], \
            self.level_text_pos_[1] + self.text_font_1_.get_sized_height() + par.STATS_VERTICAL_SPACING)
        
        # event to detect if tile needs to fall by one square due to gravity, triggered at regular time intervals
        self.gravity_tick_ev_ = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
        # event to detect if tile can soft drop, triggered at regular time intervals
        self.soft_drop_ev_ = pyg.USEREVENT + 1
        pyg.time.set_timer(self.gravity_tick_ev_, self.fall_time_interval_ms_) 
        pyg.time.set_timer(self.soft_drop_ev_, par.SOFT_DROP_TIME_INTERVAL_ms)
        
        # set up resume button
        self.resume_button_ = Button(par.RESUME_BUTTON_POS, 'Resume')

        # set up game state
        self.state = GameState()
        self.state.on("lines_completed", self.play_sfx_callback)
        self.state.on("soft_drop", self.play_sfx_callback)
        self.state.on("hard_drop", self.play_sfx_callback)
        self.state.on("rotation", self.play_sfx_callback)
        self.state.on("game_paused", self.paused_state_callback)
        self.state.on("game_resumed", self.paused_state_callback)
        self.state.on("level_up", self.level_up_callback)

        # set up current tile
        self.tile_ = Tile(self.state)
        self.tile_.on("rotation", self.play_sfx_callback)

        # start playing main theme
        self.play_main_theme()
        
        
    def process_events_and_inputs(self) -> None:
        """Calls the event handler and retrieves the user's inputs.

        """

        self.event_handler()
        self.state.get_current_keys()


    def update(self) -> None:
        """ Updates the game and tile states based on the current inputs and events.
        
        """
        
        self.state.update_pause_state(self.resume_button_.is_activated())
        if not self.state.is_game_paused():  
            self.tile_.update_position(self.state)
            self.state.delete_completed_rows()
            self.state.game_over_check()


    def event_handler(self) -> None:
        """ Processes in-game events.
        
        """
        for event in pyg.event.get():
            # pressing the "X" button terminates the application
            if event.type == pyg.QUIT:
                self.state.game_running = False
            if event.type == self.gravity_tick_ev_:
                self.tile_.is_falling = True
            if event.type == self.soft_drop_ev_:
                self.tile_.can_soft_drop = True
            if event.type == pyg.KEYUP and event.key == par.PAUSE:
                self.state.pause_key_released = True


    def play_sfx_callback(self, event: str, data: any = None) -> None:
        """ Callback function triggered to play sound effects.

        Parameters
        ----------
        event: str
            Event that triggered the callback.
        data: any
            Additional data associated with the event.
        """

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


    def paused_state_callback(self, event: str, data: any = None) -> None:
        """ Callback function triggered when the game is paused or resumed.
        Parameters
        ----------
        event: str
            Event that triggered the callback.
        data: any
            Additional data associated with the event.
        """

        if event == "game_paused":
            # Pause gravity
            pyg.time.set_timer(self.gravity_tick_ev_, 0)
            # Pause music
            pyg.mixer.music.pause()
        elif event == "game_resumed":
            # Resume gravity
            pyg.time.set_timer(self.gravity_tick_ev_, self.fall_time_interval_ms_)
            # Resume music
            pyg.mixer.music.unpause()
        else:
            pass


    def level_up_callback(self, event: str, data: any = None) -> None: 
        """ Callback function triggered when leveling up.
        Parameters
        ----------
        event: str
            Event that triggered the callback.
        data: any
            Additional data associated with the event.
        """

        if event == "level_up":
            # speed up tile descent
            self.fall_time_interval_ms_ -= par.FALL_TIME_INTERVAL_DELTA_ms
            pyg.time.set_timer(self.gravity_tick_ev_, self.fall_time_interval_ms_)
        else:
            pass


    def play_sfx(self, sfx_type: str) -> None:
        """ Plays the specified sound effect.

        Parameters
        ----------
        sfx_type: str
            Type of sound effect to be played.
        """

        if sfx_type == "rotation":
            self.rotation_sfx_.play()
        elif sfx_type == "single":
            self.single_sfx_.play()
        elif sfx_type == "double":
            self.double_sfx_.play()
        elif sfx_type == "triple":
            self.triple_sfx_.play()
        elif sfx_type == "tetris":
            self.tetris_sfx_.play()
        elif sfx_type == "soft_drop":
            pass  # TODO: add soft drop sfx
        elif sfx_type == "hard_drop":
            pass  # TODO: add hard drop sfx
        else:
            pass
        

    def play_main_theme(self) -> None:
        """ Plays the main theme in loop.
        
        """
        pyg.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
        pyg.mixer.music.set_volume(par.MUSIC_VOLUME)


    def draw_grid(self, nr_of_rows: int, nr_of_cols: int, TLC_coords: pyg.Vector2, color: tuple = par.DEFAULT_GRID_COLOR) -> None:
        """ Draws a grid at the specified position with the specified dimensions.

        Parameters
        ----------
        nr_of_rows: int
            Number of rows of the grid.
        nr_of_cols: int
            Numer of columns of the grid.
        TLC_coords: pygame.Vector2
            Coordinates of the top left corner of the grid.
        color: tuple
            RGB color of the grid lines.
        """

        # draw horizontal lines
        for row_idx in range(0, nr_of_rows + 1):
            start_coords = (TLC_coords.x, TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            end_coords = (TLC_coords.x + nr_of_cols * par.GRID_ELEM_SIZE, 
                        TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            pyg.draw.line(surface=self.game_window_, color=color, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)
        # draw vertical lines    
        for col_idx in range(0, nr_of_cols + 1):
            start_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, TLC_coords.y)
            end_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, 
                         TLC_coords.y + par.GRID_ELEM_SIZE * nr_of_rows)
            pyg.draw.line(surface=self.game_window_, color=color, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)


    def draw_block_with_borders(self, TLC_x: int, TLC_y: int, size: int, color: tuple, border_color: tuple) -> None:
        """ Draws a block with borders of the specified color at the specified position.
        
        Parameters
        ----------
        TLC_x: int
            X coordinate of the top left corner of the block.
        TLC_y: int
            Y coordinate of the top left corner of the block.
        size: int
            Size of the block (width and height).
        color: tuple
            RGB color of the block.
        border_color: tuple
            RGB color of the block border.
        """

        block = pyg.Rect(TLC_x, TLC_y, size, size)
        pyg.draw.rect(self.game_window_, color, block)
        top_left = (TLC_x, TLC_y) 
        down_left = (top_left[0], top_left[1] + size)
        down_right = (down_left[0] + size, down_left[1])
        top_right = (down_right[0], down_right[1] - size)
        pyg.draw.lines(surface=self.game_window_, color=border_color, closed=True,
                    points=[top_left, down_left, down_right, top_right],
                    width=par.BLOCK_BORDER_THICKNESS)


    def draw_board(self) -> None:
        """ Draws the board of the game.
        
        """
        for row in range (0, par.GRID_NR_OF_ROWS):
            for col in range (0, par.GRID_NR_OF_COLS):
                if self.state.get_BOM_element(row, col) != None:
                    self.draw_block_with_borders(par.GRID_TLC_x + col * par.GRID_ELEM_SIZE,
                                                 par.GRID_TLC_y + row * par.GRID_ELEM_SIZE,
                                                 par.GRID_ELEM_SIZE,
                                                 self.state.get_BOM_element(row, col),
                                                 par.WHITE)


    def draw_tile(self, tile_type: str, cfg_mat: list, pos_x: int, pos_y: int, border_color: tuple = par.WHITE) -> None:
        """ Draws a tile at the specified position.
        
        Parameters
        ----------
        tile_type: str
            Type of the tile to be drawn.
        cfg_mat: list
            Configuration matrix of the tile to be drawn.
        pos_x: int
            X coordinate of the top left corner of the tile to be drawn.
        pos_y: int
            Y coordinate of the top left corner of the tile to be drawn.
        border_color: tuple
            RGB color of the tile border.
        """

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

        drop_distance = self.tile_.compute_smallest_drop_distance(self.state)
        # draw tile outer border at drop distance
        for row in range (0, par.TILE_CONFIG_IDX_MAX):
            for col in range (0, par.TILE_CONFIG_IDX_MAX):
                if self.tile_._configuration_matrix[row][col] == 1:                  
                    if row == 0 or self.tile_._configuration_matrix[row - 1][col] == 0: # lazy OR eval allows to avoid idx overflow (same below)
                        pyg.draw.line(self.game_window_, 
                                        color, 
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)
                    if col == 0 or self.tile_._configuration_matrix[row][col - 1] == 0:
                        pyg.draw.line(self.game_window_, 
                                        color, 
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)                            
                    if row == par.TILE_CONFIG_IDX_MAX - 1 or self.tile_._configuration_matrix[row + 1][col] == 0:
                        pyg.draw.line(self.game_window_, 
                                        color, 
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)  
                    if col == par.TILE_CONFIG_IDX_MAX - 1 or self.tile_._configuration_matrix[row][col + 1] == 0:
                        pyg.draw.line(self.game_window_, 
                                        color, 
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self.tile_.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self.tile_.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)


    def draw_pause_menu(self) -> None:
        """ Draws the pause menu. 
        
        """

        # Draw transparent grey overlay
        pyg.draw.rect(self.transparent_overlay_, par.TRANSPARENT_GREY, (pyg.Vector2(0,0), pyg.Vector2(par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT)))
        self.game_window_.blit(self.transparent_overlay_, par.PAUSE_MENU_TRANSPARENT_OVERLAY_POS)
        self.resume_button_.draw(self.game_window_)
        pyg.display.update()


    def draw_frame(self) -> None:
        """ Draws the current frame.
        
        """

        # TODO: only draw tile and board each time not the entire thing
        # color background such that older tile positions do not appear
        self.game_window_.fill(par.BLACK)
        self.game_window_.blit(self.logo_, par.LOGO_POS)

        score_text_surface, _ = self.text_font_1_.render(f'Score:  {self.state.get_score()}', par.WHITE)
        level_text_surface, _ = self.text_font_1_.render(f'Level:   {self.state.get_level()}', par.WHITE)
        lines_text_surface, _ = self.text_font_1_.render(f'Lines:   {self.state.get_lines()}', par.WHITE)


        self.game_window_.blit(score_text_surface, par.STATS_POS)
        self.game_window_.blit(level_text_surface, self.level_text_pos_)
        self.game_window_.blit(lines_text_surface, self.lines_text_pos_)
        self.game_window_.blit(self.next_piece_text_surface_, par.NEXT_PIECE_TEXT_POS)

        self.game_window_.blit(self.pause_info_text_surface_, par.PAUSE_INFO_TEXT_POS)
        
        # draw next piece preview grid
        self.draw_grid(par.TILE_CONFIG_IDX_MAX, par.TILE_CONFIG_IDX_MAX, par.NEXT_PIECE_GRID_POS, par.GREY)
        # draw board grid
        self.draw_grid(par.GRID_NR_OF_ROWS, par.GRID_NR_OF_COLS, pyg.Vector2(par.GRID_TLC_x, par.GRID_TLC_y), par.GREY)
        self.draw_board()
        self.draw_tile(self.tile_.get_current_type(), 
                       self.tile_._configuration_matrix,
                       self.tile_.position.x,
                       self.tile_.position.y)
        # draw next tile preview
        self.draw_tile(self.tile_.get_next_type(),
                       par.TILE_SHAPES[self.tile_.get_next_type()][0],
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