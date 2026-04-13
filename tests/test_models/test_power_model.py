from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.models.power_model import PowerModel

_POWER_DURATION_MS: int = 5000
_AVAILABLE_POWERS: tuple[str, ...] = ("immunity", "killer")


@pytest.fixture
def power_model() -> PowerModel:
    surf: pygame.Surface = pygame.Surface((32, 32))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    with patch("pygame.image.load", return_value=mock_img):
        with patch("pygame.mixer.Sound", return_value=MagicMock()):
            return PowerModel()


class TestPowerModelInit:
    @pytest.mark.unit
    def test_is_sprite(self, power_model: PowerModel) -> None:
        assert isinstance(power_model, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_current_power_starts_empty(self, power_model: PowerModel) -> None:
        assert power_model.current_power == ""

    @pytest.mark.unit
    def test_power_reset_time_starts_none(self, power_model: PowerModel) -> None:
        assert power_model._power_reset_time is None

    @pytest.mark.unit
    def test_animation_index_starts_at_zero(self, power_model: PowerModel) -> None:
        assert power_model._animation_index == 0

    @pytest.mark.unit
    def test_has_seven_frames(self, power_model: PowerModel) -> None:
        assert len(power_model._frames) == 7

    @pytest.mark.unit
    def test_has_image(self, power_model: PowerModel) -> None:
        assert isinstance(power_model.image, pygame.Surface)

    @pytest.mark.unit
    def test_has_rect(self, power_model: PowerModel) -> None:
        assert isinstance(power_model.rect, pygame.Rect)

    @pytest.mark.unit
    def test_rect_bottom_on_ground(self, power_model: PowerModel) -> None:
        assert power_model.rect.bottom == 300

    @pytest.mark.unit
    def test_rect_x_in_spawn_range(self, power_model: PowerModel) -> None:
        assert 10 <= power_model.rect.centerx <= 730


class TestPowerModelSelectPower:
    @pytest.mark.unit
    def test_select_power_sets_valid_power(self, power_model: PowerModel) -> None:
        power_model._select_power()
        assert power_model.current_power in _AVAILABLE_POWERS

    @pytest.mark.unit
    def test_select_power_sets_reset_time(self, power_model: PowerModel) -> None:
        before: int = pygame.time.get_ticks()
        power_model._select_power()
        assert power_model._power_reset_time is not None
        assert power_model._power_reset_time >= before + _POWER_DURATION_MS

    @pytest.mark.unit
    def test_select_power_reset_time_has_correct_duration(self, power_model: PowerModel) -> None:
        before: int = pygame.time.get_ticks()
        power_model._select_power()
        after: int = pygame.time.get_ticks()
        assert before + _POWER_DURATION_MS <= power_model._power_reset_time <= after + _POWER_DURATION_MS


class TestPowerModelStopPower:
    @pytest.mark.unit
    def test_stop_power_clears_expired_power(self, power_model: PowerModel) -> None:
        power_model.current_power = "immunity"
        power_model._power_reset_time = pygame.time.get_ticks() - 1
        power_model.stop_power()
        assert power_model.current_power == ""

    @pytest.mark.unit
    def test_stop_power_keeps_active_power(self, power_model: PowerModel) -> None:
        power_model.current_power = "killer"
        power_model._power_reset_time = pygame.time.get_ticks() + 9_999_999
        power_model.stop_power()
        assert power_model.current_power == "killer"

    @pytest.mark.unit
    def test_stop_power_no_op_when_no_power(self, power_model: PowerModel) -> None:
        power_model.current_power = ""
        power_model.stop_power()
        assert power_model.current_power == ""

    @pytest.mark.unit
    def test_stop_power_no_op_when_reset_time_is_none(self, power_model: PowerModel) -> None:
        power_model.current_power = ""
        power_model._power_reset_time = None
        power_model.stop_power()
        assert power_model.current_power == ""


class TestPowerModelAnimation:
    @pytest.mark.unit
    def test_animation_state_advances_index(self, power_model: PowerModel) -> None:
        power_model._animation_state()
        assert power_model._animation_index > 0

    @pytest.mark.unit
    def test_animation_state_wraps_around(self, power_model: PowerModel) -> None:
        power_model._animation_index = 6.95
        power_model._animation_state()
        assert power_model._animation_index < 1

    @pytest.mark.unit
    def test_animation_state_updates_image(self, power_model: PowerModel) -> None:
        power_model._animation_index = 0.0
        power_model._animation_state()
        assert power_model.image is power_model._frames[int(power_model._animation_index)]
