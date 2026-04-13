from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.models.player_model import PlayerModel

_GROUND_Y: int = 300
_X_RIGHT_LIMIT: int = 735


@pytest.fixture
def player() -> PlayerModel:
    surf: pygame.Surface = pygame.Surface((50, 80))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    with patch("pygame.image.load", return_value=mock_img):
        with patch("pygame.mixer.Sound", return_value=MagicMock()):
            return PlayerModel()


class TestPlayerModelInit:
    @pytest.mark.unit
    def test_is_sprite(self, player: PlayerModel) -> None:
        assert isinstance(player, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_initial_midbottom_x(self, player: PlayerModel) -> None:
        assert player.rect.midbottom[0] == 80

    @pytest.mark.unit
    def test_initial_midbottom_y(self, player: PlayerModel) -> None:
        assert player.rect.midbottom[1] == _GROUND_Y

    @pytest.mark.unit
    def test_gravity_starts_at_zero(self, player: PlayerModel) -> None:
        assert player._gravity == 0.0

    @pytest.mark.unit
    def test_walk_index_starts_at_zero(self, player: PlayerModel) -> None:
        assert player._walk_index == 0.0

    @pytest.mark.unit
    def test_has_normal_skin(self, player: PlayerModel) -> None:
        assert "normal" in player._skins

    @pytest.mark.unit
    def test_has_immunity_skin(self, player: PlayerModel) -> None:
        assert "immunity" in player._skins

    @pytest.mark.unit
    def test_has_killer_skin(self, player: PlayerModel) -> None:
        assert "killer" in player._skins

    @pytest.mark.unit
    def test_has_image(self, player: PlayerModel) -> None:
        assert isinstance(player.image, pygame.Surface)

    @pytest.mark.unit
    def test_has_rect(self, player: PlayerModel) -> None:
        assert isinstance(player.rect, pygame.Rect)


class TestPlayerModelIsJump:
    @pytest.mark.unit
    def test_is_jump_false_when_on_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y
        assert player.is_jump is False

    @pytest.mark.unit
    def test_is_jump_true_when_above_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 10
        assert player.is_jump is True

    @pytest.mark.unit
    def test_is_jump_false_when_below_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y + 1
        assert player.is_jump is False


class TestPlayerModelGravity:
    @pytest.mark.unit
    def test_gravity_increases_when_above_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 50
        player._gravity = 0.0
        player._apply_gravity()
        assert player._gravity == 1.0

    @pytest.mark.unit
    def test_gravity_resets_when_reaching_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y
        player._gravity = 0.0
        player._apply_gravity()
        assert player._gravity == 0.0

    @pytest.mark.unit
    def test_rect_bottom_clamped_to_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y
        player._gravity = 0.0
        player._apply_gravity()
        assert player.rect.bottom == _GROUND_Y

    @pytest.mark.unit
    def test_rect_y_increases_when_above_ground(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 50
        player._gravity = 0.0
        original_y: int = player.rect.y
        player._apply_gravity()
        assert player.rect.y == original_y + 1

    @pytest.mark.unit
    def test_gravity_accumulates_across_calls(self, player: PlayerModel) -> None:
        player.rect.bottom = _GROUND_Y - 100
        player._gravity = 0.0
        player._apply_gravity()
        assert player._gravity == 1.0
        player._apply_gravity()
        assert player._gravity == 2.0


class TestPlayerModelLimits:
    @pytest.mark.unit
    def test_clamps_x_below_zero(self, player: PlayerModel) -> None:
        player.rect.x = -10
        player._limits()
        assert player.rect.x == 0

    @pytest.mark.unit
    def test_clamps_x_above_right_limit(self, player: PlayerModel) -> None:
        player.rect.x = 800
        player._limits()
        assert player.rect.x == _X_RIGHT_LIMIT

    @pytest.mark.unit
    def test_does_not_clamp_within_bounds(self, player: PlayerModel) -> None:
        player.rect.x = 100
        player._limits()
        assert player.rect.x == 100

    @pytest.mark.unit
    def test_clamps_exactly_at_right_limit(self, player: PlayerModel) -> None:
        player.rect.x = _X_RIGHT_LIMIT
        player._limits()
        assert player.rect.x == _X_RIGHT_LIMIT

    @pytest.mark.unit
    def test_clamps_exactly_at_zero(self, player: PlayerModel) -> None:
        player.rect.x = 0
        player._limits()
        assert player.rect.x == 0


class TestPlayerModelChangeSkin:
    @pytest.mark.unit
    def test_change_to_immunity_skin(self, player: PlayerModel) -> None:
        player.change_skin_player("immunity")
        assert player._walk_frames is player._skins["immunity"][0]
        assert player._jump_frame is player._skins["immunity"][1]

    @pytest.mark.unit
    def test_change_to_killer_skin(self, player: PlayerModel) -> None:
        player.change_skin_player("killer")
        assert player._walk_frames is player._skins["killer"][0]
        assert player._jump_frame is player._skins["killer"][1]

    @pytest.mark.unit
    def test_change_to_normal_skin(self, player: PlayerModel) -> None:
        player.change_skin_player("killer")
        player.change_skin_player("normal")
        assert player._walk_frames is player._skins["normal"][0]
        assert player._jump_frame is player._skins["normal"][1]

    @pytest.mark.unit
    def test_invalid_skin_falls_back_to_normal(self, player: PlayerModel) -> None:
        player.change_skin_player("nonexistent")
        assert player._walk_frames is player._skins["normal"][0]
        assert player._jump_frame is player._skins["normal"][1]

    @pytest.mark.unit
    def test_skin_immunity_differs_from_normal(self, player: PlayerModel) -> None:
        player.change_skin_player("normal")
        normal_frames: list[pygame.Surface] = player._walk_frames

        player.change_skin_player("immunity")
        immunity_frames: list[pygame.Surface] = player._walk_frames

        assert normal_frames is not immunity_frames
