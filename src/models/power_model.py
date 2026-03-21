from random import choice, randint

import pygame

from src.constants.paths import (
    GRAPHIC_MISTERY_BOX_ANIMATION_1,
    GRAPHIC_MISTERY_BOX_ANIMATION_2,
    GRAPHIC_MISTERY_BOX_ANIMATION_3,
    GRAPHIC_MISTERY_BOX_ANIMATION_4,
    GRAPHIC_MISTERY_BOX_ANIMATION_5,
    GRAPHIC_MISTERY_BOX_ANIMATION_6,
    GRAPHIC_MISTERY_BOX_ANIMATION_7,
    SOUND_PLAYER_POWER_UP,
)

_ANIM_SPEED: float = 0.1
_GROUND_Y: int = 300
_POWER_DURATION_MS: int = 5000
_AVAILABLE_POWERS: tuple[str, ...] = ("immunity", "killer")
_BOX_PATHS = (
    GRAPHIC_MISTERY_BOX_ANIMATION_1,
    GRAPHIC_MISTERY_BOX_ANIMATION_2,
    GRAPHIC_MISTERY_BOX_ANIMATION_3,
    GRAPHIC_MISTERY_BOX_ANIMATION_4,
    GRAPHIC_MISTERY_BOX_ANIMATION_5,
    GRAPHIC_MISTERY_BOX_ANIMATION_6,
    GRAPHIC_MISTERY_BOX_ANIMATION_7,
)


class PowerModel(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self._animation_index: float = 0
        self._power_reset_time: int | None = None
        self.current_power: str = ""

        self._frames: list[pygame.Surface] = [pygame.image.load(path).convert_alpha() for path in _BOX_PATHS]
        self._power_pick_sound: pygame.mixer.Sound = pygame.mixer.Sound(SOUND_PLAYER_POWER_UP)

        self.image: pygame.Surface = self._frames[0]
        self.rect: pygame.Rect = self.image.get_rect(midbottom=(randint(10, 730), _GROUND_Y))

    def _animation_state(self) -> None:
        self._animation_index = (self._animation_index + _ANIM_SPEED) % len(self._frames)
        self.image = self._frames[int(self._animation_index)]

    def _select_power(self) -> None:
        self.current_power = choice(_AVAILABLE_POWERS)
        self._power_reset_time = pygame.time.get_ticks() + _POWER_DURATION_MS

    def _pick_up(self, player: pygame.sprite.GroupSingle) -> None:
        if not pygame.sprite.collide_rect(player.sprite, self):
            return

        self._power_pick_sound.play()
        self._select_power()
        self.kill()

    def stop_power(self) -> None:
        if self.current_power and pygame.time.get_ticks() >= self._power_reset_time:
            self.current_power = ""

    def update(self, player: pygame.sprite.GroupSingle) -> None:
        self._animation_state()
        self._pick_up(player=player)
