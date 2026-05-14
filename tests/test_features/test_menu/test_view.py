from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.features.menu.view import MenuView


@pytest.fixture
def menu(surface: pygame.Surface) -> MenuView:
    surf: pygame.Surface = pygame.Surface((50, 50))
    font_surf: pygame.Surface = pygame.Surface((200, 50))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    mock_font: MagicMock = MagicMock()
    mock_font.render.return_value = font_surf
    with (
        patch("pygame.image.load", return_value=mock_img),
        patch("pygame.transform.scale2x", return_value=surf),
        patch("pygame.font.Font", return_value=mock_font),
    ):
        return MenuView(screen=surface, title="Test Title")


class TestMenuView:
    @pytest.mark.unit
    def test_instantiation_succeeds(self, menu: MenuView) -> None:
        assert menu is not None

    @pytest.mark.unit
    def test_screen_stored(self, menu: MenuView, surface: pygame.Surface) -> None:
        assert menu._screen is surface

    @pytest.mark.unit
    def test_render_with_zero_score_does_not_raise(self, menu: MenuView) -> None:
        menu.render(score=0)

    @pytest.mark.unit
    def test_render_with_positive_score_does_not_raise(self, menu: MenuView) -> None:
        menu.render(score=42)

    @pytest.mark.unit
    def test_render_default_score_is_zero(self, menu: MenuView) -> None:
        menu.render()

    @pytest.mark.unit
    def test_title_surface_stored(self, menu: MenuView) -> None:
        assert menu._title_surface is not None

    @pytest.mark.unit
    def test_title_rect_stored(self, menu: MenuView) -> None:
        assert menu._title_rect is not None

    @pytest.mark.unit
    def test_reset_surface_stored(self, menu: MenuView) -> None:
        assert menu._reset_surface is not None
