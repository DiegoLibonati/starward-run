import pygame

from src.models.bat_model import BatModel
from src.models.obstacle_model import ObstacleModel


class TestBatModelInstantiation:
    def test_instantiates_with_frames_and_y_pos(self, bat_frames: list[pygame.Surface]) -> None:
        bat = BatModel(frames=bat_frames, y_pos=210)
        assert bat is not None

    def test_is_bat_model(self, bat: BatModel) -> None:
        assert isinstance(bat, BatModel)

    def test_inherits_obstacle_model(self, bat: BatModel) -> None:
        assert isinstance(bat, ObstacleModel)

    def test_is_sprite(self, bat: BatModel) -> None:
        assert isinstance(bat, pygame.sprite.Sprite)


class TestBatModelYPos:
    def test_y_pos_stored_correctly(self, bat_frames: list[pygame.Surface]) -> None:
        bat = BatModel(frames=bat_frames, y_pos=210)
        assert bat._y_pos == 210

    def test_rect_bottom_matches_y_pos(self, bat_frames: list[pygame.Surface]) -> None:
        bat = BatModel(frames=bat_frames, y_pos=210)
        assert bat.rect.bottom == 210

    def test_custom_y_pos(self, bat_frames: list[pygame.Surface]) -> None:
        bat = BatModel(frames=bat_frames, y_pos=150)
        assert bat._y_pos == 150
        assert bat.rect.bottom == 150


class TestBatModelFrames:
    def test_frames_stored_correctly(self, bat_frames: list[pygame.Surface]) -> None:
        bat = BatModel(frames=bat_frames, y_pos=210)
        assert bat._frames == bat_frames

    def test_frames_length(self, bat: BatModel) -> None:
        assert len(bat._frames) == 2

    def test_frames_are_surfaces(self, bat: BatModel) -> None:
        for frame in bat._frames:
            assert isinstance(frame, pygame.Surface)
