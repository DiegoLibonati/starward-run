import pygame
import pytest

from src.features.obstacles.base import ObstacleModel
from src.features.obstacles.grounder import GrounderModel


class TestGrounderModel:
    @pytest.mark.unit
    def test_inherits_obstacle_model(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)

        assert isinstance(grounder, ObstacleModel)

    @pytest.mark.unit
    def test_inherits_pygame_sprite(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)

        assert isinstance(grounder, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_rect_bottom_matches_y_pos(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)

        assert grounder.rect.bottom == 300

    @pytest.mark.unit
    def test_image_is_first_frame(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)

        assert grounder.image is six_frames[0]

    @pytest.mark.unit
    def test_rect_centerx_starts_off_right_side(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)

        assert grounder.rect.centerx >= 900
