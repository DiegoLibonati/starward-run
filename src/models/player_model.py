import pygame

from src.constants.paths import (
    GRAPHIC_PLAYER_JUMP_1,
    GRAPHIC_PLAYER_JUMP_IMMUNITY_1,
    GRAPHIC_PLAYER_JUMP_KILLER_1,
    GRAPHIC_PLAYER_WALK_1,
    GRAPHIC_PLAYER_WALK_2,
    GRAPHIC_PLAYER_WALK_IMMUNITY_1,
    GRAPHIC_PLAYER_WALK_IMMUNITY_2,
    GRAPHIC_PLAYER_WALK_KILLER_1,
    GRAPHIC_PLAYER_WALK_KILLER_2,
    SOUND_PLAYER_JUMP,
)

_GROUND_Y: int = 300
_JUMP_FORCE: int = -20
_MOVE_SPEED: int = 2
_X_RIGHT_LIMIT: int = 735
_ANIM_SPEED: float = 0.1
_JUMP_VOLUME: float = 0.2


class PlayerModel(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self._walk_index: float = 0
        self._gravity: int = 0

        self._skins: dict[str, tuple[list[pygame.Surface], pygame.Surface]] = {
            "normal": (
                [
                    pygame.image.load(GRAPHIC_PLAYER_WALK_1).convert_alpha(),
                    pygame.image.load(GRAPHIC_PLAYER_WALK_2).convert_alpha(),
                ],
                pygame.image.load(GRAPHIC_PLAYER_JUMP_1).convert_alpha(),
            ),
            "immunity": (
                [
                    pygame.image.load(GRAPHIC_PLAYER_WALK_IMMUNITY_1).convert_alpha(),
                    pygame.image.load(GRAPHIC_PLAYER_WALK_IMMUNITY_2).convert_alpha(),
                ],
                pygame.image.load(GRAPHIC_PLAYER_JUMP_IMMUNITY_1).convert_alpha(),
            ),
            "killer": (
                [
                    pygame.image.load(GRAPHIC_PLAYER_WALK_KILLER_1).convert_alpha(),
                    pygame.image.load(GRAPHIC_PLAYER_WALK_KILLER_2).convert_alpha(),
                ],
                pygame.image.load(GRAPHIC_PLAYER_JUMP_KILLER_1).convert_alpha(),
            ),
        }

        self._walk_frames, self._jump_frame = self._skins["normal"]
        self._jump_sound: pygame.mixer.Sound = pygame.mixer.Sound(SOUND_PLAYER_JUMP)
        self._jump_sound.set_volume(_JUMP_VOLUME)

        self.image: pygame.Surface = self._walk_frames[0]
        self.rect: pygame.Rect = self.image.get_rect(midbottom=(80, _GROUND_Y))

    @property
    def is_jump(self) -> bool:
        return self.rect.bottom < _GROUND_Y

    def _input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.is_jump:
            self._jump_sound.play()
            self._gravity = _JUMP_FORCE
        elif keys[pygame.K_d]:
            self.rect.x += _MOVE_SPEED
        elif keys[pygame.K_a]:
            self.rect.x -= _MOVE_SPEED

    def _apply_gravity(self) -> None:
        self._gravity += 1
        self.rect.y += self._gravity

        if self.rect.bottom >= _GROUND_Y:
            self.rect.bottom = _GROUND_Y
            self._gravity = 0

    def _animation_state(self) -> None:
        if self.is_jump:
            self.image = self._jump_frame
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_d]:
            self._walk_index = (self._walk_index + _ANIM_SPEED) % len(self._walk_frames)
            self.image = self._walk_frames[int(self._walk_index)]
        else:
            self.image = self._walk_frames[0]

    def _limits(self) -> None:
        self.rect.x = max(0, min(self.rect.x, _X_RIGHT_LIMIT))

    def change_skin_player(self, power: str) -> None:
        self._walk_frames, self._jump_frame = self._skins.get(power, self._skins["normal"])

    def update(self) -> None:
        self._input()
        self._apply_gravity()
        self._animation_state()
        self._limits()
