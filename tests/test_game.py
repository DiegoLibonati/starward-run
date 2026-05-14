from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.configs.testing_config import TestingConfig
from src.game import Game


@pytest.fixture
def game(surface: pygame.Surface) -> Game:
    surf: pygame.Surface = pygame.Surface((50, 50))
    font_surf: pygame.Surface = pygame.Surface((200, 50))
    mock_img: MagicMock = MagicMock()
    mock_img.convert.return_value = surf
    mock_img.convert_alpha.return_value = surf
    mock_sound: MagicMock = MagicMock()
    mock_font: MagicMock = MagicMock()
    mock_font.render.return_value = font_surf
    config: TestingConfig = TestingConfig()
    with (
        patch("pygame.display.set_mode", return_value=surface),
        patch("pygame.display.set_caption"),
        patch("pygame.time.Clock"),
        patch("pygame.mixer.Sound", return_value=mock_sound),
        patch("pygame.font.Font", return_value=mock_font),
        patch("pygame.image.load", return_value=mock_img),
        patch("pygame.transform.scale2x", return_value=surf),
        patch("pygame.time.set_timer"),
    ):
        return Game(config=config)


class TestGame:
    @pytest.mark.unit
    def test_title_is_starward_run(self, game: Game) -> None:
        assert game.title == "Starward Run"

    @pytest.mark.unit
    def test_game_started_is_false_initially(self, game: Game) -> None:
        assert game.game_started is False

    @pytest.mark.unit
    def test_score_is_zero_initially(self, game: Game) -> None:
        assert game.score == 0

    @pytest.mark.unit
    def test_obstacles_spawn_is_empty_initially(self, game: Game) -> None:
        assert len(game.obstacles_spawn) == 0

    @pytest.mark.unit
    def test_power_is_none_initially(self, game: Game) -> None:
        assert game.power is None

    @pytest.mark.unit
    def test_player_is_not_none_after_init(self, game: Game) -> None:
        assert game.player is not None

    @pytest.mark.unit
    def test_update_obstacle_pool_always_adds_snail(self, game: Game) -> None:
        game._score = 0

        game._update_obstacle_pool()

        assert "snail" in game.obstacles_spawn

    @pytest.mark.unit
    def test_update_obstacle_pool_adds_bat_at_score_10(self, game: Game) -> None:
        game._score = 10

        game._update_obstacle_pool()

        assert "bat" in game.obstacles_spawn

    @pytest.mark.unit
    def test_update_obstacle_pool_no_bat_below_score_10(self, game: Game) -> None:
        game._obstacles_spawn = set()
        game._score = 9

        game._update_obstacle_pool()

        assert "bat" not in game.obstacles_spawn

    @pytest.mark.unit
    def test_update_obstacle_pool_adds_grounder_at_score_20(self, game: Game) -> None:
        game._score = 20

        game._update_obstacle_pool()

        assert "grounder" in game.obstacles_spawn

    @pytest.mark.unit
    def test_update_obstacle_pool_no_grounder_below_score_20(self, game: Game) -> None:
        game._obstacles_spawn = set()
        game._score = 19

        game._update_obstacle_pool()

        assert "grounder" not in game.obstacles_spawn

    @pytest.mark.unit
    def test_compute_score_returns_elapsed_seconds(self, game: Game) -> None:
        with patch("pygame.time.get_ticks", return_value=5000):
            game._start_time = 0
            result: int = game._compute_score()

        assert result == 5

    @pytest.mark.unit
    def test_compute_score_accounts_for_start_time(self, game: Game) -> None:
        with patch("pygame.time.get_ticks", return_value=10000):
            game._start_time = 3000
            result: int = game._compute_score()

        assert result == 7

    @pytest.mark.unit
    def test_collision_sprite_returns_true_when_no_obstacles(self, game: Game) -> None:
        game._power = None
        game._obstacle_group.empty()

        result: bool = game._collision_sprite()

        assert result is True

    @pytest.mark.unit
    def test_collision_sprite_immunity_power_returns_true(self, game: Game) -> None:
        mock_power: MagicMock = MagicMock()
        mock_power.current_power = "immunity"
        game._power = mock_power

        result: bool = game._collision_sprite()

        assert result is True
        mock_power.stop_power.assert_called_once()

    @pytest.mark.unit
    def test_collision_sprite_returns_false_on_direct_collision(self, game: Game) -> None:
        game._power = None
        obstacle: pygame.sprite.Sprite = pygame.sprite.Sprite()
        obstacle.image = pygame.Surface((50, 50))
        obstacle.rect = game.player.rect.copy()
        game._obstacle_group.add(obstacle)

        result: bool = game._collision_sprite()

        assert result is False

    @pytest.mark.unit
    def test_reset_game_clears_obstacles_spawn(self, game: Game) -> None:
        game._obstacles_spawn = {"snail", "bat"}
        dummy: pygame.sprite.Sprite = pygame.sprite.Sprite()
        dummy.image = pygame.Surface((50, 50))
        dummy.rect = pygame.Rect(55, 250, 50, 50)
        with patch("src.game.PlayerModel", return_value=dummy):
            game._reset_game()

        assert len(game.obstacles_spawn) == 0

    @pytest.mark.unit
    def test_reset_game_clears_power(self, game: Game) -> None:
        game._power = MagicMock()
        dummy: pygame.sprite.Sprite = pygame.sprite.Sprite()
        dummy.image = pygame.Surface((50, 50))
        dummy.rect = pygame.Rect(55, 250, 50, 50)
        with patch("src.game.PlayerModel", return_value=dummy):
            game._reset_game()

        assert game.power is None
