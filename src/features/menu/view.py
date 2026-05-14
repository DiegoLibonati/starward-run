import pygame

from src.constants.game import SCREEN_W
from src.constants.paths import FONT_PRIMARY, GRAPHIC_PLAYER_STAND_1

_FONT_SIZE: int = 50
_COLOR_TITLE: tuple[int, int, int] = (111, 196, 169)
_COLOR_BG_MENU: tuple[int, int, int] = (94, 129, 162)


class MenuView:
    def __init__(self, screen: pygame.Surface, title: str) -> None:
        self._screen = screen
        self._font = pygame.font.Font(FONT_PRIMARY, _FONT_SIZE)

        player_stand = pygame.transform.scale2x(pygame.image.load(GRAPHIC_PLAYER_STAND_1).convert_alpha())
        self._player_stand_rect = player_stand.get_rect(center=(SCREEN_W // 2, 200))
        self._player_stand_surface = player_stand

        title_surface = self._font.render(title, False, _COLOR_TITLE)
        self._title_surface = title_surface
        self._title_rect = title_surface.get_rect(center=(SCREEN_W // 2, 50))

        reset_surface = self._font.render("Reset game with SPACE", False, _COLOR_TITLE)
        self._reset_surface = reset_surface
        self._reset_rect = reset_surface.get_rect(center=(SCREEN_W // 2, 350))

    def render(self, score: int = 0) -> None:
        self._screen.fill(_COLOR_BG_MENU)
        self._screen.blit(self._player_stand_surface, self._player_stand_rect)
        self._screen.blit(self._title_surface, self._title_rect)
        self._screen.blit(self._reset_surface, self._reset_rect)

        if score:
            surface = self._font.render(f"Score: {score}", False, _COLOR_TITLE)
            self._screen.blit(surface, surface.get_rect(center=(SCREEN_W // 2, 80)))
