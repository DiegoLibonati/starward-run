import os
import sys
from unittest.mock import patch

import pytest

from src.utils.helpers import resource_path


class TestResourcePath:
    @pytest.mark.unit
    def test_returns_string(self) -> None:
        result: str = resource_path("some/file.png")
        assert isinstance(result, str)

    @pytest.mark.unit
    def test_normal_mode_returns_absolute_path(self) -> None:
        result: str = resource_path("some/file.png")
        expected: str = os.path.join(os.path.abspath("."), "some/file.png")
        assert result == expected

    @pytest.mark.unit
    def test_pyinstaller_mode_uses_meipass(self) -> None:
        with patch.object(sys, "_MEIPASS", "/tmp/bundle", create=True):
            result: str = resource_path("assets/img.png")
        assert result == os.path.join("/tmp/bundle", "assets/img.png")

    @pytest.mark.unit
    def test_empty_relative_path_returns_base(self) -> None:
        result: str = resource_path("")
        expected: str = os.path.join(os.path.abspath("."), "")
        assert result == expected

    @pytest.mark.unit
    def test_nested_path_joined_correctly(self) -> None:
        result: str = resource_path("src/assets/graphics/player.png")
        assert "src" in result and "assets" in result and "player.png" in result

    @pytest.mark.unit
    def test_pyinstaller_mode_ignores_cwd(self) -> None:
        with patch.object(sys, "_MEIPASS", "/bundle", create=True):
            result: str = resource_path("data/config.json")
        assert not result.startswith(os.path.abspath("."))
        assert result.startswith("/bundle")
