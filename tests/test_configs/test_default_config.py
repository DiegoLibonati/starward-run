import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfig:
    @pytest.mark.unit
    def test_debug_is_false(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.DEBUG is False

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.TESTING is False

    @pytest.mark.unit
    def test_tz_default(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.TZ == "America/Argentina/Buenos_Aires"

    @pytest.mark.unit
    def test_env_name_from_pytest_env(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.ENV_NAME == "template_value"

    @pytest.mark.unit
    def test_has_tz_attribute(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert hasattr(config, "TZ")

    @pytest.mark.unit
    def test_has_debug_attribute(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert hasattr(config, "DEBUG")

    @pytest.mark.unit
    def test_has_testing_attribute(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert hasattr(config, "TESTING")

    @pytest.mark.unit
    def test_has_env_name_attribute(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert hasattr(config, "ENV_NAME")
