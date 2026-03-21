import pygame

from src.models.obstacle_model import ObstacleModel
from src.models.snail_model import SnailModel


class TestSnailModelInstantiation:
    def test_instantiates_with_frames_and_y_pos(self, snail_frames: list[pygame.Surface]) -> None:
        snail = SnailModel(frames=snail_frames, y_pos=300)
        assert snail is not None

    def test_is_snail_model(self, snail: SnailModel) -> None:
        assert isinstance(snail, SnailModel)

    def test_inherits_obstacle_model(self, snail: SnailModel) -> None:
        assert isinstance(snail, ObstacleModel)

    def test_is_sprite(self, snail: SnailModel) -> None:
        assert isinstance(snail, pygame.sprite.Sprite)


class TestSnailModelYPos:
    def test_y_pos_stored_correctly(self, snail_frames: list[pygame.Surface]) -> None:
        snail = SnailModel(frames=snail_frames, y_pos=300)
        assert snail._y_pos == 300

    def test_rect_bottom_matches_y_pos(self, snail_frames: list[pygame.Surface]) -> None:
        snail = SnailModel(frames=snail_frames, y_pos=300)
        assert snail.rect.bottom == 300

    def test_custom_y_pos(self, snail_frames: list[pygame.Surface]) -> None:
        snail = SnailModel(frames=snail_frames, y_pos=250)
        assert snail._y_pos == 250
        assert snail.rect.bottom == 250


class TestSnailModelFrames:
    def test_frames_stored_correctly(self, snail_frames: list[pygame.Surface]) -> None:
        snail = SnailModel(frames=snail_frames, y_pos=300)
        assert snail._frames == snail_frames

    def test_frames_length(self, snail: SnailModel) -> None:
        assert len(snail._frames) == 2

    def test_frames_are_surfaces(self, snail: SnailModel) -> None:
        for frame in snail._frames:
            assert isinstance(frame, pygame.Surface)
