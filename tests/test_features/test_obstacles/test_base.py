import pygame
import pytest

from src.features.obstacles.base import ObstacleModel


class _ConcreteObstacle(ObstacleModel):
    pass


class TestObstacleModel:
    @pytest.mark.unit
    def test_initial_image_is_first_frame(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)

        assert obstacle.image is two_frames[0]

    @pytest.mark.unit
    def test_rect_bottom_matches_y_pos(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)

        assert obstacle.rect.bottom == 300

    @pytest.mark.unit
    def test_rect_centerx_starts_off_right_side(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)

        assert obstacle.rect.centerx >= 900

    @pytest.mark.unit
    def test_animation_index_starts_at_zero(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)

        assert obstacle._animation_index == 0.0

    @pytest.mark.unit
    def test_animation_state_advances_index(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)

        obstacle._animation_state()

        assert obstacle._animation_index > 0

    @pytest.mark.unit
    def test_animation_state_wraps_around(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        obstacle._animation_index = 1.95

        obstacle._animation_state()

        assert obstacle._animation_index < 1.0

    @pytest.mark.unit
    def test_speed_at_score_0_is_5(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=0)

        assert obstacle.rect.x == initial_x - 5

    @pytest.mark.unit
    def test_speed_at_score_50_is_5(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=50)

        assert obstacle.rect.x == initial_x - 5

    @pytest.mark.unit
    def test_speed_at_score_51_is_10(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=51)

        assert obstacle.rect.x == initial_x - 10

    @pytest.mark.unit
    def test_speed_at_score_100_is_10(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=100)

        assert obstacle.rect.x == initial_x - 10

    @pytest.mark.unit
    def test_speed_at_score_101_is_25(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=101)

        assert obstacle.rect.x == initial_x - 25

    @pytest.mark.unit
    def test_speed_at_score_200_is_25(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=200)

        assert obstacle.rect.x == initial_x - 25

    @pytest.mark.unit
    def test_speed_at_score_201_is_30(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        initial_x: int = obstacle.rect.x

        obstacle._change_obstacle_speed(score=201)

        assert obstacle.rect.x == initial_x - 30

    @pytest.mark.unit
    def test_destroy_kills_sprite_when_off_screen(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        pygame.sprite.Group(obstacle)
        obstacle.rect.x = -101

        obstacle._destroy()

        assert not obstacle.alive()

    @pytest.mark.unit
    def test_destroy_does_not_kill_when_on_screen(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        pygame.sprite.Group(obstacle)
        obstacle.rect.x = 0

        obstacle._destroy()

        assert obstacle.alive()

    @pytest.mark.unit
    def test_destroy_kills_at_exactly_boundary(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        pygame.sprite.Group(obstacle)
        obstacle.rect.x = -100

        obstacle._destroy()

        assert not obstacle.alive()

    @pytest.mark.unit
    def test_update_moves_rect_left(self, two_frames: list[pygame.Surface]) -> None:
        obstacle: _ConcreteObstacle = _ConcreteObstacle(frames=two_frames, y_pos=300)
        pygame.sprite.Group(obstacle)
        initial_x: int = obstacle.rect.x

        obstacle.update(score=0)

        assert obstacle.rect.x < initial_x
