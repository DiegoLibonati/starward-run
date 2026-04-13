from unittest.mock import MagicMock, patch

import pygame
import pytest

from src.constants.vars import get_obstacles
from src.models.bat_model import BatModel
from src.models.grounder_model import GrounderModel
from src.models.snail_model import SnailModel


@pytest.fixture
def obstacles() -> dict[str, BatModel | GrounderModel | SnailModel]:
    surf: pygame.Surface = pygame.Surface((50, 50))
    mock_img: MagicMock = MagicMock()
    mock_img.convert_alpha.return_value = surf
    with patch("pygame.image.load", return_value=mock_img):
        return get_obstacles()


class TestGetObstacles:
    @pytest.mark.unit
    def test_returns_dict_with_snail_key(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert "snail" in obstacles

    @pytest.mark.unit
    def test_returns_dict_with_bat_key(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert "bat" in obstacles

    @pytest.mark.unit
    def test_returns_dict_with_grounder_key(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert "grounder" in obstacles

    @pytest.mark.unit
    def test_returns_exactly_three_keys(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert len(obstacles) == 3

    @pytest.mark.unit
    def test_snail_is_snail_model(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert isinstance(obstacles["snail"], SnailModel)

    @pytest.mark.unit
    def test_bat_is_bat_model(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert isinstance(obstacles["bat"], BatModel)

    @pytest.mark.unit
    def test_grounder_is_grounder_model(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert isinstance(obstacles["grounder"], GrounderModel)

    @pytest.mark.unit
    def test_snail_y_pos(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert obstacles["snail"].rect.bottom == 300

    @pytest.mark.unit
    def test_bat_y_pos(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert obstacles["bat"].rect.bottom == 210

    @pytest.mark.unit
    def test_grounder_y_pos(self, obstacles: dict[str, BatModel | GrounderModel | SnailModel]) -> None:
        assert obstacles["grounder"].rect.bottom == 300

    @pytest.mark.unit
    def test_each_call_returns_new_instances(self) -> None:
        surf: pygame.Surface = pygame.Surface((50, 50))
        mock_img: MagicMock = MagicMock()
        mock_img.convert_alpha.return_value = surf
        with patch("pygame.image.load", return_value=mock_img):
            first: dict[str, BatModel | GrounderModel | SnailModel] = get_obstacles()
            second: dict[str, BatModel | GrounderModel | SnailModel] = get_obstacles()
        assert first["snail"] is not second["snail"]
