import pygame
import pytest

from src.features.obstacles.base import ObstacleModel
from src.features.obstacles.bat import BatModel


class TestBatModel:
    @pytest.mark.unit
    def test_inherits_obstacle_model(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)

        assert isinstance(bat, ObstacleModel)

    @pytest.mark.unit
    def test_inherits_pygame_sprite(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)

        assert isinstance(bat, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_rect_bottom_matches_y_pos(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)

        assert bat.rect.bottom == 210

    @pytest.mark.unit
    def test_image_is_first_frame(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)

        assert bat.image is two_frames[0]

    @pytest.mark.unit
    def test_rect_centerx_starts_off_right_side(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)

        assert bat.rect.centerx >= 900
