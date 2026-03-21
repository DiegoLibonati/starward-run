import pygame
import pytest

from src.models.bat_model import BatModel
from src.models.obstacle_model import ObstacleModel


class TestObstacleModelInit:
    def test_is_sprite(self, bat: BatModel) -> None:
        assert isinstance(bat, pygame.sprite.Sprite)

    def test_is_obstacle_model(self, bat: BatModel) -> None:
        assert isinstance(bat, ObstacleModel)

    def test_frames_stored(self, bat: BatModel, bat_frames: list[pygame.Surface]) -> None:
        assert bat._frames == bat_frames

    def test_y_pos_stored(self, bat: BatModel) -> None:
        assert bat._y_pos == 210

    def test_animation_index_is_zero(self, bat: BatModel) -> None:
        assert bat._animation_index == 0.0

    def test_image_is_surface(self, bat: BatModel) -> None:
        assert isinstance(bat.image, pygame.Surface)

    def test_rect_is_rect(self, bat: BatModel) -> None:
        assert isinstance(bat.rect, pygame.Rect)

    def test_initial_x_within_spawn_range(self, bat: BatModel) -> None:
        assert 900 <= bat.rect.centerx <= 1100 + bat.rect.width

    def test_initial_y_matches_y_pos(self, bat: BatModel) -> None:
        assert bat.rect.bottom == 210


class TestObstacleModelSpeedStages:
    @pytest.mark.parametrize(
        "score,expected_speed",
        [
            (0, 5),
            (50, 5),
            (51, 10),
            (100, 10),
            (101, 25),
            (200, 25),
            (201, 30),
            (999, 30),
        ],
    )
    def test_speed_at_score(self, bat_frames: list[pygame.Surface], score: int, expected_speed: int) -> None:
        obstacle = BatModel(frames=bat_frames, y_pos=210)
        initial_x = obstacle.rect.x
        obstacle._change_obstacle_speed(score=score)
        assert obstacle.rect.x == initial_x - expected_speed


class TestObstacleModelDestroy:
    def test_kill_when_off_screen(self, bat: BatModel) -> None:
        group = pygame.sprite.Group(bat)
        bat.rect.x = -101
        bat._destroy()
        assert len(group) == 0

    def test_no_kill_when_at_boundary(self, bat: BatModel) -> None:
        group = pygame.sprite.Group(bat)
        bat.rect.x = -100
        bat._destroy()
        assert len(group) == 0

    def test_no_kill_when_on_screen(self, bat: BatModel) -> None:
        group = pygame.sprite.Group(bat)
        bat.rect.x = 0
        bat._destroy()
        assert len(group) == 1


class TestObstacleModelAnimation:
    def test_animation_index_advances(self, bat: BatModel) -> None:
        initial_index = bat._animation_index
        bat._animation_state()
        assert bat._animation_index > initial_index

    def test_animation_index_wraps_around(self, bat_frames: list[pygame.Surface]) -> None:
        obstacle = BatModel(frames=bat_frames, y_pos=210)
        obstacle._animation_index = 1.95
        obstacle._animation_state()
        assert obstacle._animation_index < 1.0

    def test_image_updates_after_animation(self, bat: BatModel) -> None:
        bat._animation_index = 0.95
        bat._animation_state()
        assert isinstance(bat.image, pygame.Surface)


class TestObstacleModelUpdate:
    def test_update_moves_obstacle_left(self, bat: BatModel) -> None:
        initial_x = bat.rect.x
        bat.update(score=0)
        assert bat.rect.x < initial_x

    def test_update_kills_when_off_screen(self, bat: BatModel) -> None:
        group = pygame.sprite.Group(bat)
        bat.rect.x = -200
        bat.update(score=0)
        assert len(group) == 0
