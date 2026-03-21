import os
import sys

import pytest

from src.utils.helpers import resource_path


class TestResourcePathReturnType:
    def test_returns_string(self) -> None:
        assert isinstance(resource_path("some/path.png"), str)

    def test_returns_non_empty_string(self) -> None:
        assert resource_path("some/path.png") != ""


class TestResourcePathNormal:
    def test_returns_absolute_path(self) -> None:
        result = resource_path("some/path.png")
        assert os.path.isabs(result)

    def test_preserves_filename(self) -> None:
        result = resource_path("some/path.png")
        assert result.endswith("path.png")

    def test_preserves_nested_structure(self) -> None:
        result = resource_path("assets/graphics/player.png")
        assert "assets" in result
        assert "graphics" in result
        assert result.endswith("player.png")

    def test_base_is_current_directory(self) -> None:
        expected_base = os.path.abspath(".")
        result = resource_path("file.txt")
        assert result.startswith(expected_base)


class TestResourcePathPyInstaller:
    def test_uses_meipass_when_available(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "_MEIPASS", "/bundle/path", raising=False)
        result = resource_path("assets/image.png")
        assert result.startswith("/bundle/path")

    def test_meipass_path_contains_relative(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "_MEIPASS", "/bundle", raising=False)
        result = resource_path("assets/image.png")
        assert "assets" in result
        assert result.endswith("image.png")

    def test_falls_back_to_cwd_without_meipass(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delattr(sys, "_MEIPASS", raising=False)
        result = resource_path("file.txt")
        assert os.path.isabs(result)
