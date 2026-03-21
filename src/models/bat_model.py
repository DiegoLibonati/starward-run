import pygame

from src.models.obstacle_model import ObstacleModel


class BatModel(ObstacleModel):
    def __init__(self, frames: list[pygame.Surface], y_pos: int) -> None:
        super().__init__(frames=frames, y_pos=y_pos)
