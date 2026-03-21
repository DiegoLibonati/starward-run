import os

import pygame
import pytest

from src.configs.default_config import DefaultConfig
from src.models.bat_model import BatModel
from src.models.grounder_model import GrounderModel
from src.models.player_model import PlayerModel
from src.models.power_model import PowerModel
from src.models.snail_model import SnailModel
from src.ui.interface_game import InterfaceGame

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(scope="session", autouse=True)
def pygame_init() -> None:
    pygame.init()
    pygame.display.set_mode((800, 400))
    yield
    pygame.quit()


@pytest.fixture
def default_config() -> DefaultConfig:
    return DefaultConfig()


@pytest.fixture
def bat_frames() -> list[pygame.Surface]:
    return [pygame.Surface((50, 50)), pygame.Surface((50, 50))]


@pytest.fixture
def snail_frames() -> list[pygame.Surface]:
    return [pygame.Surface((50, 50)), pygame.Surface((50, 50))]


@pytest.fixture
def grounder_frames() -> list[pygame.Surface]:
    return [pygame.Surface((50, 50)) for _ in range(6)]


@pytest.fixture
def bat(bat_frames: list[pygame.Surface]) -> BatModel:
    return BatModel(frames=bat_frames, y_pos=210)


@pytest.fixture
def snail(snail_frames: list[pygame.Surface]) -> SnailModel:
    return SnailModel(frames=snail_frames, y_pos=300)


@pytest.fixture
def grounder(grounder_frames: list[pygame.Surface]) -> GrounderModel:
    return GrounderModel(frames=grounder_frames, y_pos=300)


@pytest.fixture
def player() -> PlayerModel:
    return PlayerModel()


@pytest.fixture
def power() -> PowerModel:
    return PowerModel()


@pytest.fixture
def game(default_config: DefaultConfig) -> InterfaceGame:
    return InterfaceGame(config=default_config)
