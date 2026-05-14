import pygame

from src.constants.paths import (
    GRAPHIC_BAT_ANIMATION_1,
    GRAPHIC_BAT_ANIMATION_2,
    GRAPHIC_GROUNDER_ANIMATION_1,
    GRAPHIC_GROUNDER_ANIMATION_2,
    GRAPHIC_GROUNDER_ANIMATION_3,
    GRAPHIC_GROUNDER_ANIMATION_4,
    GRAPHIC_GROUNDER_ANIMATION_5,
    GRAPHIC_GROUNDER_ANIMATION_6,
    GRAPHIC_SNAIL_ANIMATION_1,
    GRAPHIC_SNAIL_ANIMATION_2,
)
from src.features.obstacles.bat import BatModel
from src.features.obstacles.grounder import GrounderModel
from src.features.obstacles.snail import SnailModel


def get_obstacles() -> dict[str, BatModel | GrounderModel | SnailModel]:
    return {
        "snail": SnailModel(
            frames=[
                pygame.image.load(GRAPHIC_SNAIL_ANIMATION_1).convert_alpha(),
                pygame.image.load(GRAPHIC_SNAIL_ANIMATION_2).convert_alpha(),
            ],
            y_pos=300,
        ),
        "bat": BatModel(
            frames=[
                pygame.image.load(GRAPHIC_BAT_ANIMATION_1).convert_alpha(),
                pygame.image.load(GRAPHIC_BAT_ANIMATION_2).convert_alpha(),
            ],
            y_pos=210,
        ),
        "grounder": GrounderModel(
            frames=[
                pygame.image.load(GRAPHIC_GROUNDER_ANIMATION_1).convert_alpha(),
                pygame.image.load(GRAPHIC_GROUNDER_ANIMATION_2).convert_alpha(),
                pygame.image.load(GRAPHIC_GROUNDER_ANIMATION_3).convert_alpha(),
                pygame.image.load(GRAPHIC_GROUNDER_ANIMATION_4).convert_alpha(),
                pygame.image.load(GRAPHIC_GROUNDER_ANIMATION_5).convert_alpha(),
                pygame.image.load(GRAPHIC_GROUNDER_ANIMATION_6).convert_alpha(),
            ],
            y_pos=300,
        ),
    }
