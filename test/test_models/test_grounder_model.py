import pygame

from src.models.grounder_model import GrounderModel
from src.models.obstacle_model import ObstacleModel


class TestGrounderModelInstantiation:
    def test_instantiates_with_frames_and_y_pos(self, grounder_frames: list[pygame.Surface]) -> None:
        grounder = GrounderModel(frames=grounder_frames, y_pos=300)
        assert grounder is not None

    def test_is_grounder_model(self, grounder: GrounderModel) -> None:
        assert isinstance(grounder, GrounderModel)

    def test_inherits_obstacle_model(self, grounder: GrounderModel) -> None:
        assert isinstance(grounder, ObstacleModel)

    def test_is_sprite(self, grounder: GrounderModel) -> None:
        assert isinstance(grounder, pygame.sprite.Sprite)


class TestGrounderModelYPos:
    def test_y_pos_stored_correctly(self, grounder_frames: list[pygame.Surface]) -> None:
        grounder = GrounderModel(frames=grounder_frames, y_pos=300)
        assert grounder._y_pos == 300

    def test_rect_bottom_matches_y_pos(self, grounder_frames: list[pygame.Surface]) -> None:
        grounder = GrounderModel(frames=grounder_frames, y_pos=300)
        assert grounder.rect.bottom == 300

    def test_custom_y_pos(self, grounder_frames: list[pygame.Surface]) -> None:
        grounder = GrounderModel(frames=grounder_frames, y_pos=280)
        assert grounder._y_pos == 280
        assert grounder.rect.bottom == 280


class TestGrounderModelFrames:
    def test_frames_stored_correctly(self, grounder_frames: list[pygame.Surface]) -> None:
        grounder = GrounderModel(frames=grounder_frames, y_pos=300)
        assert grounder._frames == grounder_frames

    def test_frames_length_is_six(self, grounder: GrounderModel) -> None:
        assert len(grounder._frames) == 6

    def test_frames_are_surfaces(self, grounder: GrounderModel) -> None:
        for frame in grounder._frames:
            assert isinstance(frame, pygame.Surface)

    def test_more_frames_than_bat_or_snail(self, grounder: GrounderModel, bat_frames: list[pygame.Surface]) -> None:
        assert len(grounder._frames) > len(bat_frames)
