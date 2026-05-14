import pygame
import pytest

from src.features.obstacles.base import ObstacleModel
from src.features.obstacles.snail import SnailModel


class TestSnailModel:
    @pytest.mark.unit
    def test_inherits_obstacle_model(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)

        assert isinstance(snail, ObstacleModel)

    @pytest.mark.unit
    def test_inherits_pygame_sprite(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)

        assert isinstance(snail, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_rect_bottom_matches_y_pos(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)

        assert snail.rect.bottom == 300

    @pytest.mark.unit
    def test_image_is_first_frame(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)

        assert snail.image is two_frames[0]

    @pytest.mark.unit
    def test_rect_centerx_starts_off_right_side(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)

        assert snail.rect.centerx >= 900
