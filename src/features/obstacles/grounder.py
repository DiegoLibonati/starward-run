import pygame

from src.features.obstacles.base import ObstacleModel


class GrounderModel(ObstacleModel):
    def __init__(self, frames: list[pygame.Surface], y_pos: int) -> None:
        super().__init__(frames=frames, y_pos=y_pos)
