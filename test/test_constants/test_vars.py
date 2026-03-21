import pygame

from src.constants.vars import get_obstacles
from src.models.bat_model import BatModel
from src.models.grounder_model import GrounderModel
from src.models.obstacle_model import ObstacleModel
from src.models.snail_model import SnailModel


class TestGetObstaclesReturnType:
    def test_returns_dict(self) -> None:
        result = get_obstacles()
        assert isinstance(result, dict)

    def test_returns_three_entries(self) -> None:
        result = get_obstacles()
        assert len(result) == 3

    def test_keys_are_strings(self) -> None:
        result = get_obstacles()
        for key in result:
            assert isinstance(key, str)


class TestGetObstaclesKeys:
    def test_has_snail_key(self) -> None:
        assert "snail" in get_obstacles()

    def test_has_bat_key(self) -> None:
        assert "bat" in get_obstacles()

    def test_has_grounder_key(self) -> None:
        assert "grounder" in get_obstacles()

    def test_exact_keys(self) -> None:
        assert set(get_obstacles().keys()) == {"snail", "bat", "grounder"}


class TestGetObstaclesValues:
    def test_snail_is_snail_model(self) -> None:
        assert isinstance(get_obstacles()["snail"], SnailModel)

    def test_bat_is_bat_model(self) -> None:
        assert isinstance(get_obstacles()["bat"], BatModel)

    def test_grounder_is_grounder_model(self) -> None:
        assert isinstance(get_obstacles()["grounder"], GrounderModel)

    def test_all_values_inherit_obstacle_model(self) -> None:
        for obstacle in get_obstacles().values():
            assert isinstance(obstacle, ObstacleModel)

    def test_all_values_are_sprites(self) -> None:
        for obstacle in get_obstacles().values():
            assert isinstance(obstacle, pygame.sprite.Sprite)


class TestGetObstaclesIndependentInstances:
    def test_each_call_returns_new_instances(self) -> None:
        first: dict[str, BatModel | GrounderModel | SnailModel] = get_obstacles()
        second: dict[str, BatModel | GrounderModel | SnailModel] = get_obstacles()
        assert first["snail"] is not second["snail"]
        assert first["bat"] is not second["bat"]
        assert first["grounder"] is not second["grounder"]
