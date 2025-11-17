import pygame as pyg
import parameters as par

class Button():
	""" Class representing a clickable button.

	"""

	def __init__(self, TLC_coords: tuple, text: str = '', font_size: int = par.DEFAULT_BUTTON_FONT_SIZE, text_color: tuple = par.BLACK) -> None:
		""" Initializes the button.
		
		Parameters
		----------
		TLC_coords : tuple
			Coordinates of the top-left corner of the button.
		text : str, optional
			Text to display on the button.
		font_size : int, optional
			Font size of the button text.
		text_color : tuple, optional
			Color of the button text.

		"""

		text_font = pyg.freetype.SysFont(pyg.freetype.get_default_font(), font_size)
		self.text_surface, _ = text_font.render(text, text_color)
		self.rect = pyg.Rect(TLC_coords[0], TLC_coords[1], 
						self.text_surface.get_width() + par.TEXT_TO_BUTTON_BORDER_SPACING,
						self.text_surface.get_height() + par.TEXT_TO_BUTTON_BORDER_SPACING)
		self.mouse_over = False
		self.clicked = False

	def update_button_state(self) -> None:
		""" Updates the button state based on mouse position and clicks.
		
		"""

		# get mouse position
		mouse_pos = pyg.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.mouse_over = True
			if pyg.mouse.get_pressed()[0] == 1 and not self.clicked: # left mouse button
				self.clicked = True
			elif pyg.mouse.get_pressed()[0] == 0 and self.clicked:
				self.clicked = False
		else:
			self.mouse_over = False
			self.clicked = False

	def is_activated(self) -> bool:
		""" Checks if the button has been clicked.

		"""

		clicked_old = self.clicked
		self.update_button_state()
		if clicked_old and not self.clicked and self.mouse_over:
			return True
		else:
			return False

	def draw(self, surface, colors: dict = par.DEFAULT_BUTTON_COLORS, border_radius: int = par.DEFAULT_BUTTON_BORDER_RADIUS) -> None:
		""" Draws the button on the given surface.
		
		Parameters
		----------
		surface : pygame.Surface
			The surface to draw the button on.
		colors : dict, optional
			Dictionary containing colors for different button states.
		border_radius : int, optional
			Border radius for the button corners.

		"""
		
		# TODO: check border radius validity -> should not be larger than half the smallest side of the button
		self.update_button_state()
		if not self.mouse_over:
			pyg.draw.rect(surface, colors["button_idle"], self.rect, border_radius=border_radius)
		elif self.mouse_over and not self.clicked:
			pyg.draw.rect(surface, colors["button_hover"], self.rect, border_radius=border_radius)
		else:
			pyg.draw.rect(surface, colors["button_active"], self.rect, border_radius=border_radius)

		surface.blit(self.text_surface, (self.rect.centerx - self.text_surface.get_width() // 2,
										self.rect.centery - self.text_surface.get_height() // 2))