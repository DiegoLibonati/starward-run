import pygame
import pytest

from src.models.obstacle_model import ObstacleModel
from src.models.snail_model import SnailModel


class TestSnailModel:
    @pytest.mark.unit
    def test_instantiation(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        assert snail is not None

    @pytest.mark.unit
    def test_is_sprite(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        assert isinstance(snail, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_is_obstacle_model(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        assert isinstance(snail, ObstacleModel)

    @pytest.mark.unit
    def test_y_pos_set_correctly(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        assert snail.rect.bottom == 300

    @pytest.mark.unit
    def test_custom_y_pos(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=250)
        assert snail.rect.bottom == 250

    @pytest.mark.unit
    def test_has_image(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        assert isinstance(snail.image, pygame.Surface)

    @pytest.mark.unit
    def test_has_rect(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        assert isinstance(snail.rect, pygame.Rect)

    @pytest.mark.unit
    def test_can_be_added_to_group(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        group: pygame.sprite.Group = pygame.sprite.Group(snail)
        assert snail in group.sprites()

    @pytest.mark.unit
    def test_update_moves_left(self, two_frames: list[pygame.Surface]) -> None:
        snail: SnailModel = SnailModel(frames=two_frames, y_pos=300)
        initial_x: int = snail.rect.x
        snail.update(score=0)
        assert snail.rect.x < initial_x
