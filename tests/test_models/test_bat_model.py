import pygame
import pytest

from src.models.bat_model import BatModel
from src.models.obstacle_model import ObstacleModel


class TestBatModel:
    @pytest.mark.unit
    def test_instantiation(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert bat is not None

    @pytest.mark.unit
    def test_is_sprite(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert isinstance(bat, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_is_obstacle_model(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert isinstance(bat, ObstacleModel)

    @pytest.mark.unit
    def test_y_pos_set_correctly(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert bat.rect.bottom == 210

    @pytest.mark.unit
    def test_custom_y_pos(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=150)
        assert bat.rect.bottom == 150

    @pytest.mark.unit
    def test_has_image(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert isinstance(bat.image, pygame.Surface)

    @pytest.mark.unit
    def test_has_rect(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        assert isinstance(bat.rect, pygame.Rect)

    @pytest.mark.unit
    def test_can_be_added_to_group(self, two_frames: list[pygame.Surface]) -> None:
        bat: BatModel = BatModel(frames=two_frames, y_pos=210)
        group: pygame.sprite.Group = pygame.sprite.Group(bat)
        assert bat in group.sprites()
