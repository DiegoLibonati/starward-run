from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.configs.default_config import DefaultConfig
from src.ui.interface_game import InterfaceGame


class _FakePlayer(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.is_jump = False

    def update(self) -> None:
        pass

    def change_skin_player(self, power: str) -> None:
        pass


class _FakeObstacle(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, score: int) -> None:
        pass


@pytest.fixture
def game() -> Generator[InterfaceGame, None, None]:
    surf: pygame.Surface = pygame.Surface((10, 10))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    mock_img.convert.return_value = surf
    mock_img.get_rect.return_value = pygame.Rect(0, 0, 10, 10)

    mock_font_instance: MagicMock = MagicMock()
    mock_font_instance.render.return_value = MagicMock(get_rect=lambda **kw: pygame.Rect(0, 0, 100, 50))

    config: DefaultConfig = DefaultConfig()

    with (
        patch("pygame.image.load", return_value=mock_img),
        patch("pygame.mixer.Sound", return_value=MagicMock()),
        patch("pygame.font.Font", return_value=mock_font_instance),
        patch("pygame.transform.scale2x", return_value=surf),
        patch("src.ui.interface_game.PlayerModel", side_effect=lambda: _FakePlayer()),
    ):
        yield InterfaceGame(config=config)


class TestInterfaceGameInit:
    @pytest.mark.unit
    def test_title_is_starward_run(self, game: InterfaceGame) -> None:
        assert game.title == "StarwardRun"

    @pytest.mark.unit
    def test_game_started_is_false(self, game: InterfaceGame) -> None:
        assert game.game_started is False

    @pytest.mark.unit
    def test_score_starts_at_zero(self, game: InterfaceGame) -> None:
        assert game.score == 0

    @pytest.mark.unit
    def test_start_time_is_zero(self, game: InterfaceGame) -> None:
        assert game.start_time == 0

    @pytest.mark.unit
    def test_obstacles_spawn_starts_empty(self, game: InterfaceGame) -> None:
        assert len(game.obstacles_spawn) == 0

    @pytest.mark.unit
    def test_power_starts_none(self, game: InterfaceGame) -> None:
        assert game.power is None

    @pytest.mark.unit
    def test_player_single_group_has_player(self, game: InterfaceGame) -> None:
        assert game.player is not None

    @pytest.mark.unit
    def test_obstacle_group_starts_empty(self, game: InterfaceGame) -> None:
        assert len(game.obstacle_group.sprites()) == 0

    @pytest.mark.unit
    def test_screen_is_surface(self, game: InterfaceGame) -> None:
        assert isinstance(game.screen, pygame.Surface)

    @pytest.mark.unit
    def test_clock_is_clock(self, game: InterfaceGame) -> None:
        assert isinstance(game.clock, pygame.time.Clock)


class TestInterfaceGameObstaclePool:
    @pytest.mark.unit
    def test_pool_always_includes_snail(self, game: InterfaceGame) -> None:
        game._score = 0
        game._update_obstacle_pool()
        assert "snail" in game.obstacles_spawn

    @pytest.mark.unit
    def test_pool_excludes_bat_below_threshold(self, game: InterfaceGame) -> None:
        game._score = 9
        game._obstacles_spawn = set()
        game._update_obstacle_pool()
        assert "bat" not in game.obstacles_spawn

    @pytest.mark.unit
    def test_pool_includes_bat_at_threshold(self, game: InterfaceGame) -> None:
        game._score = 10
        game._obstacles_spawn = set()
        game._update_obstacle_pool()
        assert "bat" in game.obstacles_spawn

    @pytest.mark.unit
    def test_pool_includes_bat_above_threshold(self, game: InterfaceGame) -> None:
        game._score = 15
        game._obstacles_spawn = set()
        game._update_obstacle_pool()
        assert "bat" in game.obstacles_spawn

    @pytest.mark.unit
    def test_pool_excludes_grounder_below_threshold(self, game: InterfaceGame) -> None:
        game._score = 19
        game._obstacles_spawn = set()
        game._update_obstacle_pool()
        assert "grounder" not in game.obstacles_spawn

    @pytest.mark.unit
    def test_pool_includes_grounder_at_threshold(self, game: InterfaceGame) -> None:
        game._score = 20
        game._obstacles_spawn = set()
        game._update_obstacle_pool()
        assert "grounder" in game.obstacles_spawn

    @pytest.mark.unit
    def test_pool_includes_all_at_high_score(self, game: InterfaceGame) -> None:
        game._score = 100
        game._obstacles_spawn = set()
        game._update_obstacle_pool()
        assert game.obstacles_spawn == {"snail", "bat", "grounder"}


class TestInterfaceGameComputeScore:
    @pytest.mark.unit
    def test_score_is_zero_at_start(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks()
        assert game._compute_score() == 0

    @pytest.mark.unit
    def test_score_reflects_elapsed_seconds(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks() - 5000
        assert game._compute_score() == 5

    @pytest.mark.unit
    def test_score_uses_integer_division(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks() - 1500
        assert game._compute_score() == 1

    @pytest.mark.unit
    def test_score_increases_with_time(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks() - 3000
        score_a: int = game._compute_score()
        game._start_time = pygame.time.get_ticks() - 6000
        score_b: int = game._compute_score()
        assert score_b > score_a


class TestInterfaceGameReset:
    @pytest.mark.unit
    def test_reset_clears_obstacles_spawn(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = {"snail", "bat"}
        game._reset_game()
        assert game._obstacles_spawn == set()

    @pytest.mark.unit
    def test_reset_clears_power(self, game: InterfaceGame) -> None:
        game._power = MagicMock()
        game._reset_game()
        assert game._power is None

    @pytest.mark.unit
    def test_reset_empties_power_group(self, game: InterfaceGame) -> None:
        game._reset_game()
        assert len(game.power_single_group.sprites()) == 0

    @pytest.mark.unit
    def test_reset_adds_new_player(self, game: InterfaceGame) -> None:
        game._reset_game()
        assert game.player is not None

    @pytest.mark.unit
    def test_reset_replaces_player_group(self, game: InterfaceGame) -> None:
        player_before: pygame.sprite.Sprite | None = game.player
        game._reset_game()
        player_after: pygame.sprite.Sprite | None = game.player
        assert player_after is not player_before


class TestInterfaceGameCollision:
    @pytest.mark.unit
    def test_no_collision_no_power_returns_true(self, game: InterfaceGame) -> None:
        game._power = None
        obstacle: _FakeObstacle = _FakeObstacle(x=9999, y=9999)
        game._obstacle_group.add(obstacle)
        result: bool = game._collision_sprite()
        assert result is True
        game._obstacle_group.remove(obstacle)

    @pytest.mark.unit
    def test_collision_no_power_returns_false(self, game: InterfaceGame) -> None:
        game._power = None
        player: pygame.sprite.Sprite = game.player_single_group.sprite
        obstacle: _FakeObstacle = _FakeObstacle(x=player.rect.x, y=player.rect.y)
        game._obstacle_group.add(obstacle)
        result: bool = game._collision_sprite()
        assert result is False
        game._obstacle_group.empty()

    @pytest.mark.unit
    def test_immunity_power_returns_true_without_checking_collision(self, game: InterfaceGame) -> None:
        mock_power: MagicMock = MagicMock()
        mock_power.current_power = "immunity"
        game._power = mock_power
        result: bool = game._collision_sprite()
        assert result is True
        mock_power.stop_power.assert_called_once()
        game._power = None

    @pytest.mark.unit
    def test_immunity_power_calls_stop_power(self, game: InterfaceGame) -> None:
        mock_power: MagicMock = MagicMock()
        mock_power.current_power = "immunity"
        game._power = mock_power
        game._collision_sprite()
        mock_power.stop_power.assert_called_once()
        game._power = None

    @pytest.mark.unit
    def test_killer_power_with_collision_returns_true(self, game: InterfaceGame) -> None:
        mock_power: MagicMock = MagicMock()
        mock_power.current_power = "killer"
        game._power = mock_power
        player: pygame.sprite.Sprite = game.player_single_group.sprite
        obstacle: _FakeObstacle = _FakeObstacle(x=player.rect.x, y=player.rect.y)
        game._obstacle_group.add(obstacle)
        result: bool = game._collision_sprite()
        assert result is True
        game._obstacle_group.empty()
        game._power = None

    @pytest.mark.unit
    def test_killer_power_destroys_colliding_obstacle(self, game: InterfaceGame) -> None:
        mock_power: MagicMock = MagicMock()
        mock_power.current_power = "killer"
        game._power = mock_power
        player: pygame.sprite.Sprite = game.player_single_group.sprite
        obstacle: _FakeObstacle = _FakeObstacle(x=player.rect.x, y=player.rect.y)
        game._obstacle_group.add(obstacle)
        game._collision_sprite()
        assert obstacle not in game._obstacle_group.sprites()
        game._obstacle_group.empty()
        game._power = None

    @pytest.mark.unit
    def test_collision_clears_obstacle_group(self, game: InterfaceGame) -> None:
        game._power = None
        player: pygame.sprite.Sprite = game.player_single_group.sprite
        obstacle: _FakeObstacle = _FakeObstacle(x=player.rect.x, y=player.rect.y)
        game._obstacle_group.add(obstacle)
        game._collision_sprite()
        assert len(game._obstacle_group.sprites()) == 0
