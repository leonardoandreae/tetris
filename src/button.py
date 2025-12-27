import pygame as pyg
import parameters as par


class Button():
	"""Class representing a clickable button.

	Stores rendered text, rectangle bounds and mouse state. Provides helpers
	to update input state, draw the button and check its activation.

	"""


	def __init__(self, TLC_coords: tuple, text: str = '', font_size: int = par.DEFAULT_BUTTON_FONT_SIZE, text_color: tuple = par.BLACK) -> None:
		"""Initializes the Button.

		@param TLC_coords Coordinates of the top-left corner of the button.
		@param text Text to display on the button.
		@param font_size Font size of the button text.
		@param text_color Color of the button text.
		@returns None.

		"""

		text_font = pyg.freetype.SysFont(pyg.freetype.get_default_font(), font_size)
		## Rendered pygame Surface for the button text. Used when blitting the label.
		self._text_surface, _ = text_font.render(text, text_color)
		## Bounding rect of the button.
		self._rect = pyg.Rect(TLC_coords[0], TLC_coords[1], 
						self._text_surface.get_width() + par.TEXT_TO_BUTTON_BORDER_SPACING,
						self._text_surface.get_height() + par.TEXT_TO_BUTTON_BORDER_SPACING)
		## True if the mouse is currently over the button.
		self._mouse_over = False
		## True if the button is currently clicked.
		self._clicked = False


	def _update_button_state(self) -> None:
		"""Updates the mouse-over and clicked states.

		@returns None.

		"""

		# get mouse position
		mouse_pos = pyg.mouse.get_pos()
		if self._rect.collidepoint(mouse_pos):
			self._mouse_over = True
			if pyg.mouse.get_pressed()[0] == 1 and not self._clicked: # left mouse button
				self._clicked = True
			elif pyg.mouse.get_pressed()[0] == 0 and self._clicked:
				self._clicked = False
		else:
			self._mouse_over = False
			self._clicked = False


	def is_activated(self) -> bool:
		"""Checks if the button has been activated (by clicking and releasing).

		@returns True if activated, False otherwise.
		
		"""

		clicked_old = self._clicked
		self._update_button_state()
		if clicked_old and not self._clicked and self._mouse_over:
			return True
		else:
			return False


	def draw(self, surface: pyg.Surface, colors: dict = par.DEFAULT_BUTTON_COLORS, border_radius: int = par.DEFAULT_BUTTON_BORDER_RADIUS) -> None:
		"""Draws the button on the provided surface.

		@param surface Surface where the button will be drawn.
		@param colors button colors (state dependent).
		@param border_radius Corner radius for the rounded rect.
		@returns None.

		"""
		
		# TODO: check border radius validity -> should not be larger than half the smallest side of the button
		self._update_button_state()
		if not self._mouse_over:
			pyg.draw.rect(surface, colors["button_idle"], self._rect, border_radius=border_radius)
		elif self._mouse_over and not self._clicked:
			pyg.draw.rect(surface, colors["button_hover"], self._rect, border_radius=border_radius)
		else:
			pyg.draw.rect(surface, colors["button_active"], self._rect, border_radius=border_radius)

		surface.blit(self._text_surface, (self._rect.centerx - self._text_surface.get_width() // 2,
										self._rect.centery - self._text_surface.get_height() // 2))
