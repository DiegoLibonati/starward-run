from abc import ABC
from random import randint

import pygame

_ANIM_SPEED: float = 0.1
_DESTROY_X: int = -100
_SPEED_STAGES: tuple[tuple[int, int], ...] = (
    (50, 5),
    (100, 10),
    (200, 25),
)
_SPEED_MAX: int = 30


class ObstacleModel(pygame.sprite.Sprite, ABC):
    def __init__(self, frames: list[pygame.Surface], y_pos: int) -> None:
        super().__init__()

        self._frames: list[pygame.Surface] = frames
        self._y_pos: int = y_pos
        self._animation_index: float = 0

        self.image: pygame.Surface = self._frames[0]
        self.rect: pygame.Rect = self.image.get_rect(midbottom=(randint(900, 1100), self._y_pos))

    def _animation_state(self) -> None:
        self._animation_index = (self._animation_index + _ANIM_SPEED) % len(self._frames)
        self.image = self._frames[int(self._animation_index)]

    def _change_obstacle_speed(self, score: int) -> None:
        for threshold, speed in _SPEED_STAGES:
            if score <= threshold:
                self.rect.x -= speed
                return
        self.rect.x -= _SPEED_MAX

    def _destroy(self) -> None:
        if self.rect.x <= _DESTROY_X:
            self.kill()

    def update(self, score: int) -> None:
        self._animation_state()
        self._change_obstacle_speed(score=score)
        self._destroy()
