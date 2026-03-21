import pygame

from src.models.bat_model import BatModel
from src.models.player_model import PlayerModel
from src.models.power_model import PowerModel
from src.ui.interface_game import InterfaceGame

_SCREEN_WIDTH: int = 800
_SCREEN_HEIGHT: int = 400
_SCORE_UNLOCK_BAT: int = 10
_SCORE_UNLOCK_GROUNDER: int = 20


class TestInterfaceGameInit:
    def test_game_not_started_initially(self, game: InterfaceGame) -> None:
        assert game.game_started is False

    def test_score_zero_initially(self, game: InterfaceGame) -> None:
        assert game.score == 0

    def test_start_time_zero_initially(self, game: InterfaceGame) -> None:
        assert game.start_time == 0

    def test_obstacles_spawn_empty_initially(self, game: InterfaceGame) -> None:
        assert game.obstacles_spawn == set()

    def test_power_none_initially(self, game: InterfaceGame) -> None:
        assert game.power is None

    def test_title_is_string(self, game: InterfaceGame) -> None:
        assert isinstance(game.title, str)

    def test_title_is_not_empty(self, game: InterfaceGame) -> None:
        assert game.title != ""

    def test_player_group_has_one_sprite(self, game: InterfaceGame) -> None:
        assert len(game.player_single_group) == 1

    def test_player_is_player_model(self, game: InterfaceGame) -> None:
        assert isinstance(game.player, PlayerModel)

    def test_obstacle_group_is_empty_initially(self, game: InterfaceGame) -> None:
        assert len(game.obstacle_group) == 0

    def test_power_group_is_empty_initially(self, game: InterfaceGame) -> None:
        assert len(game.power_single_group) == 0

    def test_screen_is_surface(self, game: InterfaceGame) -> None:
        assert isinstance(game.screen, pygame.Surface)

    def test_screen_dimensions(self, game: InterfaceGame) -> None:
        assert game.screen.get_width() == _SCREEN_WIDTH
        assert game.screen.get_height() == _SCREEN_HEIGHT

    def test_clock_is_clock(self, game: InterfaceGame) -> None:
        assert isinstance(game.clock, pygame.time.Clock)


class TestInterfaceGameProperties:
    def test_game_started_is_bool(self, game: InterfaceGame) -> None:
        assert isinstance(game.game_started, bool)

    def test_score_is_int(self, game: InterfaceGame) -> None:
        assert isinstance(game.score, int)

    def test_obstacles_spawn_is_set(self, game: InterfaceGame) -> None:
        assert isinstance(game.obstacles_spawn, set)

    def test_power_is_none_or_power_model(self, game: InterfaceGame) -> None:
        assert game.power is None or isinstance(game.power, PowerModel)

    def test_obstacle_group_is_group(self, game: InterfaceGame) -> None:
        assert isinstance(game.obstacle_group, pygame.sprite.Group)

    def test_player_single_group_is_group_single(self, game: InterfaceGame) -> None:
        assert isinstance(game.player_single_group, pygame.sprite.GroupSingle)

    def test_power_single_group_is_group_single(self, game: InterfaceGame) -> None:
        assert isinstance(game.power_single_group, pygame.sprite.GroupSingle)


class TestInterfaceGameResetGame:
    def test_clears_obstacles_spawn(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = {"snail", "bat", "grounder"}
        game._reset_game()
        assert game._obstacles_spawn == set()

    def test_clears_power(self, game: InterfaceGame) -> None:
        game._power = PowerModel()
        game._reset_game()
        assert game._power is None

    def test_clears_power_group(self, game: InterfaceGame) -> None:
        power = PowerModel()
        game._power_single_group.add(power)
        game._reset_game()
        assert len(game._power_single_group) == 0

    def test_recreates_player(self, game: InterfaceGame) -> None:
        old_player = game._player_single_group.sprite
        game._reset_game()
        new_player = game._player_single_group.sprite
        assert old_player is not new_player

    def test_player_group_still_has_one_sprite(self, game: InterfaceGame) -> None:
        game._reset_game()
        assert len(game._player_single_group) == 1

    def test_new_player_is_player_model(self, game: InterfaceGame) -> None:
        game._reset_game()
        assert isinstance(game._player_single_group.sprite, PlayerModel)

    def test_new_player_starts_at_ground(self, game: InterfaceGame) -> None:
        game._reset_game()
        assert game._player_single_group.sprite.rect.bottom == 300

    def test_can_be_called_multiple_times(self, game: InterfaceGame) -> None:
        game._reset_game()
        game._reset_game()
        assert len(game._player_single_group) == 1


class TestInterfaceGameComputeScore:
    def test_returns_zero_at_start(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks()
        assert game._compute_score() == 0

    def test_returns_int(self, game: InterfaceGame) -> None:
        assert isinstance(game._compute_score(), int)

    def test_score_advances_over_time(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks() - 3000
        assert game._compute_score() == 3

    def test_score_is_non_negative(self, game: InterfaceGame) -> None:
        game._start_time = pygame.time.get_ticks()
        assert game._compute_score() >= 0


class TestInterfaceGameUpdateObstaclePool:
    def test_snail_always_added(self, game: InterfaceGame) -> None:
        game._score = 0
        game._update_obstacle_pool()
        assert "snail" in game._obstacles_spawn

    def test_bat_not_added_below_threshold(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = set()
        game._score = _SCORE_UNLOCK_BAT - 1
        game._update_obstacle_pool()
        assert "bat" not in game._obstacles_spawn

    def test_bat_added_at_threshold(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = set()
        game._score = _SCORE_UNLOCK_BAT
        game._update_obstacle_pool()
        assert "bat" in game._obstacles_spawn

    def test_bat_added_above_threshold(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = set()
        game._score = _SCORE_UNLOCK_BAT + 5
        game._update_obstacle_pool()
        assert "bat" in game._obstacles_spawn

    def test_grounder_not_added_below_threshold(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = set()
        game._score = _SCORE_UNLOCK_GROUNDER - 1
        game._update_obstacle_pool()
        assert "grounder" not in game._obstacles_spawn

    def test_grounder_added_at_threshold(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = set()
        game._score = _SCORE_UNLOCK_GROUNDER
        game._update_obstacle_pool()
        assert "grounder" in game._obstacles_spawn

    def test_all_obstacles_available_at_max_score(self, game: InterfaceGame) -> None:
        game._obstacles_spawn = set()
        game._score = 100
        game._update_obstacle_pool()
        assert game._obstacles_spawn == {"snail", "bat", "grounder"}

    def test_pool_uses_set_no_duplicates(self, game: InterfaceGame) -> None:
        game._score = 100
        game._update_obstacle_pool()
        game._update_obstacle_pool()
        assert len(game._obstacles_spawn) == 3


class TestInterfaceGameCollisionSprite:
    def test_returns_true_when_no_obstacles(self, game: InterfaceGame) -> None:
        game._obstacle_group.empty()
        assert game._collision_sprite() is True

    def test_immunity_returns_true_on_collision(self, game: InterfaceGame, bat_frames: list[pygame.Surface]) -> None:
        power = PowerModel()
        power.current_power = "immunity"
        power._power_reset_time = pygame.time.get_ticks() + 5000
        game._power = power

        obstacle = BatModel(frames=bat_frames, y_pos=300)
        obstacle.rect.center = game._player_single_group.sprite.rect.center
        game._obstacle_group.add(obstacle)

        result = game._collision_sprite()
        assert result is True

    def test_collision_without_power_returns_false(self, game: InterfaceGame, bat_frames: list[pygame.Surface]) -> None:
        game._power = None

        obstacle = BatModel(frames=bat_frames, y_pos=300)
        obstacle.rect.center = game._player_single_group.sprite.rect.center
        game._obstacle_group.add(obstacle)

        result = game._collision_sprite()
        assert result is False

    def test_collision_empties_obstacle_group(self, game: InterfaceGame, bat_frames: list[pygame.Surface]) -> None:
        game._power = None

        obstacle = BatModel(frames=bat_frames, y_pos=300)
        obstacle.rect.center = game._player_single_group.sprite.rect.center
        game._obstacle_group.add(obstacle)

        game._collision_sprite()
        assert len(game._obstacle_group) == 0

    def test_killer_kills_colliding_obstacle(self, game: InterfaceGame, bat_frames: list[pygame.Surface]) -> None:
        power = PowerModel()
        power.current_power = "killer"
        power._power_reset_time = pygame.time.get_ticks() + 5000
        game._power = power

        obstacle = BatModel(frames=bat_frames, y_pos=300)
        obstacle.rect.center = game._player_single_group.sprite.rect.center
        game._obstacle_group.add(obstacle)

        result = game._collision_sprite()
        assert result is True
        assert len(game._obstacle_group) == 0
