import pygame
import pytest

from src.models.grounder_model import GrounderModel
from src.models.obstacle_model import ObstacleModel


class TestGrounderModel:
    @pytest.mark.unit
    def test_instantiation(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert grounder is not None

    @pytest.mark.unit
    def test_is_sprite(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert isinstance(grounder, pygame.sprite.Sprite)

    @pytest.mark.unit
    def test_is_obstacle_model(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert isinstance(grounder, ObstacleModel)

    @pytest.mark.unit
    def test_y_pos_set_correctly(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert grounder.rect.bottom == 300

    @pytest.mark.unit
    def test_custom_y_pos(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=280)
        assert grounder.rect.bottom == 280

    @pytest.mark.unit
    def test_stores_all_six_frames(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert len(grounder._frames) == 6

    @pytest.mark.unit
    def test_has_image(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert isinstance(grounder.image, pygame.Surface)

    @pytest.mark.unit
    def test_has_rect(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        assert isinstance(grounder.rect, pygame.Rect)

    @pytest.mark.unit
    def test_can_be_added_to_group(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        group: pygame.sprite.Group = pygame.sprite.Group(grounder)
        assert grounder in group.sprites()

    @pytest.mark.unit
    def test_update_moves_left(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        initial_x: int = grounder.rect.x
        grounder.update(score=0)
        assert grounder.rect.x < initial_x

    @pytest.mark.unit
    def test_animation_cycles_through_six_frames(self, six_frames: list[pygame.Surface]) -> None:
        grounder: GrounderModel = GrounderModel(frames=six_frames, y_pos=300)
        grounder._animation_index = 5.95
        grounder._animation_state()
        assert grounder._animation_index < 1
