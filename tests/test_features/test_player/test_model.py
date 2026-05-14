from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.constants.game import GROUND_Y
from src.features.player.model import PlayerModel


@pytest.fixture
def player(surface: pygame.Surface) -> PlayerModel:
    surf: pygame.Surface = pygame.Surface((50, 80))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    mock_sound: MagicMock = MagicMock()
    with patch("pygame.image.load", return_value=mock_img), patch("pygame.mixer.Sound", return_value=mock_sound):
        return PlayerModel()


class TestPlayerModel:
    @pytest.mark.unit
    def test_is_pygame_sprite(self, player: PlayerModel) -> None:
        assert isinstance(player, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_rect_bottom_at_ground_y(self, player: PlayerModel) -> None:
        assert player.rect.bottom == GROUND_Y

    @pytest.mark.unit
    def test_rect_centerx_at_initial_position(self, player: PlayerModel) -> None:
        assert player.rect.midbottom[0] == 80

    @pytest.mark.unit
    def test_is_jump_false_on_ground(self, player: PlayerModel) -> None:
        assert player.is_jump is False

    @pytest.mark.unit
    def test_is_jump_true_when_above_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = GROUND_Y - 10

        assert player.is_jump is True

    @pytest.mark.unit
    def test_apply_gravity_increases_gravity_value(self, player: PlayerModel) -> None:
        player._gravity = -10.0

        player._apply_gravity()

        assert player._gravity == -9.0

    @pytest.mark.unit
    def test_apply_gravity_resets_at_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = GROUND_Y + 10

        player._apply_gravity()

        assert player._gravity == 0
        assert player.rect.bottom == GROUND_Y

    @pytest.mark.unit
    def test_limits_clamps_rect_x_to_zero(self, player: PlayerModel) -> None:
        player.rect.x = -50

        player._limits()

        assert player.rect.x == 0

    @pytest.mark.unit
    def test_limits_clamps_rect_x_to_max(self, player: PlayerModel) -> None:
        player.rect.x = 1000

        player._limits()

        assert player.rect.x == 735

    @pytest.mark.unit
    def test_limits_does_not_clamp_within_bounds(self, player: PlayerModel) -> None:
        player.rect.x = 400

        player._limits()

        assert player.rect.x == 400

    @pytest.mark.unit
    def test_change_skin_sets_immunity_frames(self, player: PlayerModel) -> None:
        player.change_skin_player(power="immunity")

        assert player._walk_frames is player._skins["immunity"][0]
        assert player._jump_frame is player._skins["immunity"][1]

    @pytest.mark.unit
    def test_change_skin_sets_killer_frames(self, player: PlayerModel) -> None:
        player.change_skin_player(power="killer")

        assert player._walk_frames is player._skins["killer"][0]
        assert player._jump_frame is player._skins["killer"][1]

    @pytest.mark.unit
    def test_change_skin_unknown_falls_back_to_normal(self, player: PlayerModel) -> None:
        player.change_skin_player(power="unknown_power")

        assert player._walk_frames is player._skins["normal"][0]
        assert player._jump_frame is player._skins["normal"][1]

    @pytest.mark.unit
    def test_skins_has_three_entries(self, player: PlayerModel) -> None:
        assert set(player._skins.keys()) == {"normal", "immunity", "killer"}
