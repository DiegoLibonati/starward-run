from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.constants.game import GROUND_Y
from src.features.power.model import PowerModel


@pytest.fixture
def power(surface: pygame.Surface) -> PowerModel:
    surf: pygame.Surface = pygame.Surface((32, 32))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    mock_sound: MagicMock = MagicMock()
    with patch("pygame.image.load", return_value=mock_img), patch("pygame.mixer.Sound", return_value=mock_sound):
        return PowerModel()


class TestPowerModel:
    @pytest.mark.unit
    def test_is_pygame_sprite(self, power: PowerModel) -> None:
        assert isinstance(power, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_current_power_starts_empty(self, power: PowerModel) -> None:
        assert power.current_power == ""

    @pytest.mark.unit
    def test_power_reset_time_starts_none(self, power: PowerModel) -> None:
        assert power._power_reset_time is None

    @pytest.mark.unit
    def test_animation_index_starts_at_zero(self, power: PowerModel) -> None:
        assert power._animation_index == 0.0

    @pytest.mark.unit
    def test_rect_bottom_at_ground_y(self, power: PowerModel) -> None:
        assert power.rect.bottom == GROUND_Y

    @pytest.mark.unit
    def test_seven_frames_loaded(self, power: PowerModel) -> None:
        assert len(power._frames) == 7

    @pytest.mark.unit
    def test_animation_state_advances_index(self, power: PowerModel) -> None:
        power._animation_state()

        assert power._animation_index > 0

    @pytest.mark.unit
    def test_animation_state_wraps_around(self, power: PowerModel) -> None:
        power._animation_index = 6.95

        power._animation_state()

        assert power._animation_index < 1.0

    @pytest.mark.unit
    def test_stop_power_clears_current_power_when_expired(self, power: PowerModel) -> None:
        power.current_power = "immunity"
        power._power_reset_time = 0

        power.stop_power()

        assert power.current_power == ""

    @pytest.mark.unit
    def test_stop_power_does_not_clear_when_not_expired(self, power: PowerModel) -> None:
        power.current_power = "immunity"
        power._power_reset_time = pygame.time.get_ticks() + 99999

        power.stop_power()

        assert power.current_power == "immunity"

    @pytest.mark.unit
    def test_stop_power_does_nothing_when_no_active_power(self, power: PowerModel) -> None:
        power.current_power = ""
        power._power_reset_time = 0

        power.stop_power()

        assert power.current_power == ""

    @pytest.mark.unit
    def test_select_power_sets_valid_power(self, power: PowerModel) -> None:
        power._select_power()

        assert power.current_power in ("immunity", "killer")

    @pytest.mark.unit
    def test_select_power_sets_reset_time_in_future(self, power: PowerModel) -> None:
        power._select_power()

        assert power._power_reset_time is not None
        assert power._power_reset_time > pygame.time.get_ticks()
