import pygame as pyg
import parameters as par
from tile import *
from state import *
from button import *

class GameInterface:
    """Main interface to the game.

    Provides the game loop integration, rendering helpers, input/event handling
    and audio/UI resources used to run the Tetris application.

    """

    def __init__(self) -> None:
        """Initializes the game interface.

        @returns None.
        
        """
        
        pyg.init() # initialize pygame modules
        
        ## pygame display Surface for the main game window.
        self._game_window = pyg.display.set_mode((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT))
        pyg.display.set_caption(f"Tetris v{par.APP_VERSION}")
        
        
        ## Game window icon Surface.
        self._icon = pyg.image.load('assets/tetris_icon.png') # https://www.freepik.com/icons/tetris Icon by Freepik
        pyg.display.set_icon(self._icon)
        
        
        ## Game logo Surface (scaled).
        self._logo = pyg.image.load('assets/tetris_logo.png')
        self._logo = pyg.transform.smoothscale_by(self._logo, par.LOGO_SCALE_FACTOR)
        
        
        ## First font object for rendering text.
        self._text_font_1 = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_1)
        ## Second font object for rendering text.
        self._text_font_2 = pyg.freetype.SysFont(pyg.freetype.get_default_font(), par.FONT_SIZE_2)
        
        
        # Set up music and sfx

        pyg.mixer.music.load('assets/tetris-theme.mp3')
        ## Rotation sound effect
        self._rotation_sfx = pyg.mixer.Sound('assets/rotation.mp3')
        ## Single line clear sound effect
        self._single_sfx = pyg.mixer.Sound('assets/single.mp3')
        ## Double line clear sound effect
        self._double_sfx = pyg.mixer.Sound('assets/double.mp3')
        ## Triple line clear sound effect
        self._triple_sfx = pyg.mixer.Sound('assets/triple.mp3')
        ## Tetris (4 lines) clear sound effect
        self._tetris_sfx = pyg.mixer.Sound('assets/tetris.mp3')
        
        ## Current gravity/fall interval in milliseconds.
        self._fall_time_interval_ms = par.INITIAL_FALL_TIME_INTERVAL_ms
        
        # set up time invariant surfaces

        ## Transparent overlay surface for pause menu.
        self._transparent_overlay = pyg.Surface((par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT), pyg.SRCALPHA)
        ## Surface for pause information text.
        self._pause_info_text_surface, _ = self._text_font_1.render(f'Press "Esc" to pause the game', par.WHITE)
        ## Surface for the next tile in queue text.
        self._next_piece_text_surface, _ = self._text_font_2.render(f'Next:', par.WHITE)
        
        # precompute text positions
        ## Level text position
        self._level_text_pos = (par.STATS_POS[0], \
            par.STATS_POS[1] + self._text_font_1.get_sized_height() + par.STATS_VERTICAL_SPACING)
        ## Lines text position
        self._lines_text_pos = (self._level_text_pos[0], \
            self._level_text_pos[1] + self._text_font_1.get_sized_height() + par.STATS_VERTICAL_SPACING)
        
        ## Event to detect if tile needs to fall by one square due to gravity, triggered at regular time intervals
        self._gravity_tick_ev = pyg.USEREVENT + 0 # event ID = 24 (up to 32, but first 23 are used by pygame already)
        ## Event to detect if tile can soft drop, triggered at regular time intervals
        self._soft_drop_ev = pyg.USEREVENT + 1
        pyg.time.set_timer(self._gravity_tick_ev, self._fall_time_interval_ms) 
        pyg.time.set_timer(self._soft_drop_ev, par.SOFT_DROP_TIME_INTERVAL_ms)
        
        ## Resume button (shown in pause menu).
        self._resume_button = Button(par.RESUME_BUTTON_POS, 'Resume')

        ## Current game state
        self.state = GameState()
        self.state.on("lines_completed", self._play_sfx_callback)
        self.state.on("soft_drop", self._play_sfx_callback)
        self.state.on("hard_drop", self._play_sfx_callback)
        self.state.on("rotation", self._play_sfx_callback)
        self.state.on("game_paused", self._paused_state_callback)
        self.state.on("game_resumed", self._paused_state_callback)
        self.state.on("level_up", self._level_up_callback)

        ## Current tetromino tile.
        self._tile = Tile(self.state)
        self._tile.on("rotation", self._play_sfx_callback)

        # start playing main theme
        self._play_main_theme()
        
        
    def process_events_and_inputs(self) -> None:
        """Calls the event handler and retrieves the user's inputs.

        @returns None.

        """

        self._event_handler()
        self.state.get_current_keys()


    def update(self) -> None:
        """ Updates the game and tile states based on the current inputs and events.

        @returns None.
        
        """
        
        self.state.update_pause_state(self._resume_button.is_activated())
        if not self.state.is_game_paused():  
            self._tile.update_position(self.state)
            self.state.delete_completed_rows()
            self.state.game_over_check()


    def _event_handler(self) -> None:
        """ Processes in-game events.

        @returns None.
        
        """
        for event in pyg.event.get():
            # pressing the "X" button terminates the application
            if event.type == pyg.QUIT:
                self.state.game_running = False
            if event.type == self._gravity_tick_ev:
                self._tile.is_falling = True
            if event.type == self._soft_drop_ev:
                self._tile.can_soft_drop = True
            if event.type == pyg.KEYUP and event.key == par.PAUSE:
                self.state.pause_key_released = True


    def _play_sfx_callback(self, event: str, data: any = None) -> None:
        """Callback triggered to play sound effects.

        @param event Name of the event that triggered this callback.
        @param data Optional additional data associated with the event.
        @returns None.

        """

        if event == "rotation":
            self._play_sfx("rotation")
        elif event == "lines_completed":
            sfx_map = {
                1: "single",
                2: "double",
                3: "triple",
                4: "tetris"
            }
            if data in sfx_map:
                self._play_sfx(sfx_map[data])
        elif event == "soft_drop":
            pass  # TODO: add soft drop sfx
        elif event == "hard_drop":
            pass  # TODO: add hard drop sfx
        else:
            pass


    def _paused_state_callback(self, event: str, data: any = None) -> None:
        """Callback invoked when the game paused state changes.

        @param event Event name.
        @param data Optional data.
        @returns None.
        """

        if event == "game_paused":
            # Pause gravity
            pyg.time.set_timer(self._gravity_tick_ev, 0)
            # Pause music
            pyg.mixer.music.pause()
        elif event == "game_resumed":
            # Resume gravity
            pyg.time.set_timer(self._gravity_tick_ev, self._fall_time_interval_ms)
            # Resume music
            pyg.mixer.music.unpause()
        else:
            pass


    def _level_up_callback(self, event: str, data: any = None) -> None: 
        """Callback invoked when level-up occurs.

        @param event Event name.
        @param data Optional data.
        @returns None.

        """

        if event == "level_up":
            # speed up tile descent
            self._fall_time_interval_ms -= par.FALL_TIME_INTERVAL_DELTA_ms
            pyg.time.set_timer(self._gravity_tick_ev, self._fall_time_interval_ms)
        else:
            pass


    def _play_sfx(self, sfx_type: str) -> None:
        """Plays the specified sound effect.

        @param sfx_type Type/name of the sound effect to play.
        @returns None.

        """

        if sfx_type == "rotation":
            self._rotation_sfx.play()
        elif sfx_type == "single":
            self._single_sfx.play()
        elif sfx_type == "double":
            self._double_sfx.play()
        elif sfx_type == "triple":
            self._triple_sfx.play()
        elif sfx_type == "tetris":
            self._tetris_sfx.play()
        elif sfx_type == "soft_drop":
            pass  # TODO: add soft drop sfx
        elif sfx_type == "hard_drop":
            pass  # TODO: add hard drop sfx
        else:
            pass
        

    def _play_main_theme(self) -> None:
        """ Plays the main theme in loop.
        
        
        
        """
        pyg.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
        pyg.mixer.music.set_volume(par.MUSIC_VOLUME)


    def _draw_grid(self, nr_of_rows: int, nr_of_cols: int, TLC_coords: pyg.Vector2, color: tuple = par.DEFAULT_GRID_COLOR) -> None:
        """Draws a grid at the specified position with the specified dimensions.

        @param nr_of_rows Number of grid rows.
        @param nr_of_cols Number of grid columns.
        @param TLC_coords Top-left corner coordinates.
        @param color RGB color of grid lines.
        @returns None.

        """

        # draw horizontal lines
        for row_idx in range(0, nr_of_rows + 1):
            start_coords = (TLC_coords.x, TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            end_coords = (TLC_coords.x + nr_of_cols * par.GRID_ELEM_SIZE, 
                        TLC_coords.y + row_idx * par.GRID_ELEM_SIZE)
            pyg.draw.line(surface=self._game_window, color=color, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)
        # draw vertical lines    
        for col_idx in range(0, nr_of_cols + 1):
            start_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, TLC_coords.y)
            end_coords = (TLC_coords.x + col_idx * par.GRID_ELEM_SIZE, 
                         TLC_coords.y + par.GRID_ELEM_SIZE * nr_of_rows)
            pyg.draw.line(surface=self._game_window, color=color, 
                        start_pos=start_coords, end_pos=end_coords,
                        width=par.GRID_THICKNESS)


    def _draw_block_with_borders(self, TLC_x: int, TLC_y: int, size: int, color: tuple, border_color: tuple) -> None:
        """Draws a filled block with a border at the given TLC coordinates.

        @param TLC_x X coordinate of the block top-left corner in pixels.
        @param TLC_y Y coordinate of the block top-left corner in pixels.
        @param size Size (width and height) of the block in pixels.
        @param color Fill RGB color.
        @param border_color Border RGB color.
        @returns None.

        """

        block = pyg.Rect(TLC_x, TLC_y, size, size)
        pyg.draw.rect(self._game_window, color, block)
        top_left = (TLC_x, TLC_y) 
        down_left = (top_left[0], top_left[1] + size)
        down_right = (down_left[0] + size, down_left[1])
        top_right = (down_right[0], down_right[1] - size)
        pyg.draw.lines(surface=self._game_window, color=border_color, closed=True,
                    points=[top_left, down_left, down_right, top_right],
                    width=par.BLOCK_BORDER_THICKNESS)


    def _draw_board(self) -> None:
        """Draw the current board from the occupancy matrix.

        @returns None.

        """

        for row in range (0, par.GRID_NR_OF_ROWS):
            for col in range (0, par.GRID_NR_OF_COLS):
                if self.state.get_BOM_element(row, col) != None:
                    self._draw_block_with_borders(par.GRID_TLC_x + col * par.GRID_ELEM_SIZE,
                                                 par.GRID_TLC_y + row * par.GRID_ELEM_SIZE,
                                                 par.GRID_ELEM_SIZE,
                                                 self.state.get_BOM_element(row, col),
                                                 par.WHITE)


    def _draw_tile(self, tile_type: str, cfg_mat: list, pos_x: int, pos_y: int, border_color: tuple = par.WHITE) -> None:
        """Draws a tile of the given type and configuration at the specified position.

        @param tile_type Tile type.
        @param cfg_mat Configuration matrix of the tile.
        @param pos_x Top-left corner x-position in pixels.
        @param pos_y Top-left corner y-position in pixels.
        @param border_color RGB border color.
        @returns None.

        """

        # draw tile with its border
        for col in range (0, par.TILE_CONFIG_IDX_MAX):
            for row in range (0, par.TILE_CONFIG_IDX_MAX):
                if cfg_mat[row][col] == 1:
                    self._draw_block_with_borders(pos_x + par.GRID_ELEM_SIZE * col,
                                                pos_y + par.GRID_ELEM_SIZE * row,
                                                par.GRID_ELEM_SIZE,
                                                par.TILE_COLORS[tile_type],
                                                border_color)


    def _draw_dropped_tile_preview(self, color: tuple = par.WHITE) -> None:
        """Draws the outline of where the current tile would land if dropped immediately.

        @param color RGB color used for the outline.
        @returns None.

        """

        drop_distance = self._tile.compute_smallest_drop_distance(self.state)
        # draw tile outer border at drop distance
        for row in range (0, par.TILE_CONFIG_IDX_MAX):
            for col in range (0, par.TILE_CONFIG_IDX_MAX):
                if self._tile._configuration_matrix[row][col] == 1:                  
                    if row == 0 or self._tile._configuration_matrix[row - 1][col] == 0: # lazy OR eval allows to avoid idx overflow (same below)
                        pyg.draw.line(self._game_window, 
                                        color, 
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)
                    if col == 0 or self._tile._configuration_matrix[row][col - 1] == 0:
                        pyg.draw.line(self._game_window, 
                                        color, 
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)                            
                    if row == par.TILE_CONFIG_IDX_MAX - 1 or self._tile._configuration_matrix[row + 1][col] == 0:
                        pyg.draw.line(self._game_window, 
                                        color, 
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * col, 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)  
                    if col == par.TILE_CONFIG_IDX_MAX - 1 or self._tile._configuration_matrix[row][col + 1] == 0:
                        pyg.draw.line(self._game_window, 
                                        color, 
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + drop_distance)),
                                        pyg.Vector2(self._tile.position.x + par.GRID_ELEM_SIZE * (col + 1), 
                                                    self._tile.position.y + par.GRID_ELEM_SIZE * (row + 1 + drop_distance)),
                                        par.DROPPED_BLOCK_PREVIEW_BORDER)


    def _draw_pause_menu(self) -> None:
        """Draws the pause menu.

        @returns None.
        
        """

        # Draw transparent grey overlay
        pyg.draw.rect(self._transparent_overlay, par.TRANSPARENT_GREY, (pyg.Vector2(0,0), pyg.Vector2(par.GAME_WINDOW_WIDTH, par.GAME_WINDOW_HEIGHT)))
        self._game_window.blit(self._transparent_overlay, par.PAUSE_MENU_TRANSPARENT_OVERLAY_POS)
        self._resume_button.draw(self._game_window)
        pyg.display.update()


    def draw_frame(self) -> None:
        """ Draws the current frame.

        @returns None.
        
        """

        # TODO: only draw tile and board each time not the entire thing
        # color background such that older tile positions do not appear
        self._game_window.fill(par.BLACK)
        self._game_window.blit(self._logo, par.LOGO_POS)

        score_text_surface, _ = self._text_font_1.render(f'Score:  {self.state.get_score()}', par.WHITE)
        level_text_surface, _ = self._text_font_1.render(f'Level:   {self.state.get_level()}', par.WHITE)
        lines_text_surface, _ = self._text_font_1.render(f'Lines:   {self.state.get_lines()}', par.WHITE)


        self._game_window.blit(score_text_surface, par.STATS_POS)
        self._game_window.blit(level_text_surface, self._level_text_pos)
        self._game_window.blit(lines_text_surface, self._lines_text_pos)
        self._game_window.blit(self._next_piece_text_surface, par.NEXT_PIECE_TEXT_POS)

        self._game_window.blit(self._pause_info_text_surface, par.PAUSE_INFO_TEXT_POS)
        
        # draw next piece preview grid
        self._draw_grid(par.TILE_CONFIG_IDX_MAX, par.TILE_CONFIG_IDX_MAX, par.NEXT_PIECE_GRID_POS, par.GREY)
        # draw board grid
        self._draw_grid(par.GRID_NR_OF_ROWS, par.GRID_NR_OF_COLS, pyg.Vector2(par.GRID_TLC_x, par.GRID_TLC_y), par.GREY)
        self._draw_board()
        self._draw_tile(self._tile.get_current_type(), 
                       self._tile._configuration_matrix,
                       self._tile.position.x,
                       self._tile.position.y)
        # draw next tile preview
        self._draw_tile(self._tile.get_next_type(),
                       par.TILE_SHAPES[self._tile.get_next_type()][0],
                       par.NEXT_PIECE_GRID_POS.x,
                       par.NEXT_PIECE_GRID_POS.y)
        self._draw_dropped_tile_preview()

        if self.state.is_game_paused():
            self._draw_pause_menu()
        '''
        After calling the drawing functions to make the display Surface object look the way you want
        you must call update() to make the display Surface actually appear on the user’s monitor.
        '''
        if not self.state.is_game_paused():
            pyg.display.update()