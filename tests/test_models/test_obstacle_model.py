import pygame
import pytest

from src.models.bat_model import BatModel
from src.models.obstacle_model import ObstacleModel


class TestObstacleModelInit:
    @pytest.mark.unit
    def test_image_is_first_frame(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert bat.image is two_frames[0]

    @pytest.mark.unit
    def test_rect_bottom_equals_y_pos(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert bat.rect.bottom == 210

    @pytest.mark.unit
    def test_rect_midx_in_spawn_range(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert 900 <= bat.rect.centerx <= 1100

    @pytest.mark.unit
    def test_animation_index_starts_at_zero(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert bat._animation_index == 0

    @pytest.mark.unit
    def test_frames_stored(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert bat._frames is two_frames

    @pytest.mark.unit
    def test_is_sprite_instance(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert isinstance(bat, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_is_obstacle_model_instance(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert isinstance(bat, ObstacleModel)


class TestObstacleModelSpeed:
    @pytest.mark.unit
    def test_speed_5_when_score_is_zero(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=0)
        assert bat.rect.x == initial_x - 5

    @pytest.mark.unit
    def test_speed_5_when_score_is_50(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=50)
        assert bat.rect.x == initial_x - 5

    @pytest.mark.unit
    def test_speed_10_when_score_is_51(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=51)
        assert bat.rect.x == initial_x - 10

    @pytest.mark.unit
    def test_speed_10_when_score_is_100(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=100)
        assert bat.rect.x == initial_x - 10

    @pytest.mark.unit
    def test_speed_25_when_score_is_101(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=101)
        assert bat.rect.x == initial_x - 25

    @pytest.mark.unit
    def test_speed_25_when_score_is_200(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=200)
        assert bat.rect.x == initial_x - 25

    @pytest.mark.unit
    def test_speed_30_when_score_is_201(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=201)
        assert bat.rect.x == initial_x - 30

    @pytest.mark.unit
    def test_speed_30_when_score_is_very_high(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat._change_obstacle_speed(score=9999)
        assert bat.rect.x == initial_x - 30


class TestObstacleModelDestroy:
    @pytest.mark.unit
    def test_destroy_kills_when_at_boundary(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat.rect.x = -100
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        bat._destroy()
        assert len(group.sprites()) == 0

    @pytest.mark.unit
    def test_destroy_kills_when_past_boundary(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat.rect.x = -200
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        bat._destroy()
        assert len(group.sprites()) == 0

    @pytest.mark.unit
    def test_destroy_keeps_alive_when_at_zero(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat.rect.x = 0
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        bat._destroy()
        assert len(group.sprites()) == 1

    @pytest.mark.unit
    def test_destroy_keeps_alive_when_on_screen(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat.rect.x = 400
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        bat._destroy()
        assert len(group.sprites()) == 1

    @pytest.mark.unit
    def test_destroy_keeps_alive_just_before_boundary(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat.rect.x = -99
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        bat._destroy()
        assert len(group.sprites()) == 1


class TestObstacleModelAnimation:
    @pytest.mark.unit
    def test_animation_state_advances_index(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat._animation_state()
        assert bat._animation_index > 0

    @pytest.mark.unit
    def test_animation_state_wraps_around(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat._animation_index = 1.95
        bat._animation_state()
        assert bat._animation_index < 1

    @pytest.mark.unit
    def test_animation_state_updates_image(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat._animation_index = 0.95
        bat._animation_state()
        assert bat.image is two_frames[int(bat._animation_index)]


class TestObstacleModelUpdate:
    @pytest.mark.unit
    def test_update_decrements_x(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        initial_x: int = bat.rect.x
        bat.update(score=0)
        assert bat.rect.x < initial_x

    @pytest.mark.unit
    def test_update_kills_when_off_screen(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        bat.rect.x = -100
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        bat.update(score=0)
        assert len(group.sprites()) == 0
