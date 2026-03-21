import pygame

from src.models.power_model import PowerModel

_GROUND_Y: int = 300
_AVAILABLE_POWERS: tuple[str, ...] = ("immunity", "killer")


class TestPowerModelInit:
    def test_is_sprite(self, power: PowerModel) -> None:
        assert isinstance(power, pygame.sprite.Sprite)

    def test_initial_current_power_is_empty(self, power: PowerModel) -> None:
        assert power.current_power == ""

    def test_initial_reset_time_is_none(self, power: PowerModel) -> None:
        assert power._power_reset_time is None

    def test_animation_index_is_zero(self, power: PowerModel) -> None:
        assert power._animation_index == 0.0

    def test_frames_has_seven_entries(self, power: PowerModel) -> None:
        assert len(power._frames) == 7

    def test_frames_are_surfaces(self, power: PowerModel) -> None:
        for frame in power._frames:
            assert isinstance(frame, pygame.Surface)

    def test_image_is_surface(self, power: PowerModel) -> None:
        assert isinstance(power.image, pygame.Surface)

    def test_rect_is_rect(self, power: PowerModel) -> None:
        assert isinstance(power.rect, pygame.Rect)

    def test_rect_bottom_is_ground(self, power: PowerModel) -> None:
        assert power.rect.bottom == _GROUND_Y

    def test_rect_x_within_spawn_range(self, power: PowerModel) -> None:
        assert 10 <= power.rect.centerx <= 730 + power.rect.width


class TestPowerModelSelectPower:
    def test_sets_a_valid_power(self, power: PowerModel) -> None:
        power._select_power()
        assert power.current_power in _AVAILABLE_POWERS

    def test_sets_reset_time_as_int(self, power: PowerModel) -> None:
        power._select_power()
        assert isinstance(power._power_reset_time, int)

    def test_reset_time_is_in_the_future(self, power: PowerModel) -> None:
        power._select_power()
        assert power._power_reset_time > pygame.time.get_ticks()

    def test_reset_time_is_approximately_five_seconds_ahead(self, power: PowerModel) -> None:
        now = pygame.time.get_ticks()
        power._select_power()
        assert 4900 <= power._power_reset_time - now <= 5100

    def test_current_power_is_string(self, power: PowerModel) -> None:
        power._select_power()
        assert isinstance(power.current_power, str)


class TestPowerModelStopPower:
    def test_clears_power_after_expiry(self, power: PowerModel) -> None:
        power.current_power = "immunity"
        power._power_reset_time = pygame.time.get_ticks() - 1
        power.stop_power()
        assert power.current_power == ""

    def test_keeps_power_when_not_expired(self, power: PowerModel) -> None:
        power.current_power = "killer"
        power._power_reset_time = pygame.time.get_ticks() + 5000
        power.stop_power()
        assert power.current_power == "killer"

    def test_does_nothing_when_no_active_power(self, power: PowerModel) -> None:
        power.current_power = ""
        power._power_reset_time = pygame.time.get_ticks() - 1
        power.stop_power()
        assert power.current_power == ""

    def test_works_for_killer_power(self, power: PowerModel) -> None:
        power.current_power = "killer"
        power._power_reset_time = pygame.time.get_ticks() - 1
        power.stop_power()
        assert power.current_power == ""

    def test_works_for_immunity_power(self, power: PowerModel) -> None:
        power.current_power = "immunity"
        power._power_reset_time = pygame.time.get_ticks() - 1
        power.stop_power()
        assert power.current_power == ""


class TestPowerModelAnimation:
    def test_animation_index_advances(self, power: PowerModel) -> None:
        initial = power._animation_index
        power._animation_state()
        assert power._animation_index > initial

    def test_animation_index_wraps_around(self, power: PowerModel) -> None:
        power._animation_index = 6.95
        power._animation_state()
        assert power._animation_index < 1.0

    def test_image_is_surface_after_animation(self, power: PowerModel) -> None:
        power._animation_state()
        assert isinstance(power.image, pygame.Surface)
