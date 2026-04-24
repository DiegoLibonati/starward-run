import os

import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(scope="session", autouse=True)
def pygame_init() -> None:
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture(scope="session")
def surface() -> pygame.Surface:
    return pygame.display.set_mode((800, 600))


@pytest.fixture
def two_frames() -> list[pygame.Surface]:
    return [pygame.Surface((50, 50)), pygame.Surface((50, 50))]


@pytest.fixture
def six_frames() -> list[pygame.Surface]:
    return [pygame.Surface((60, 60)) for _ in range(6)]


@pytest.fixture
def seven_frames() -> list[pygame.Surface]:
    return [pygame.Surface((32, 32)) for _ in range(7)]
