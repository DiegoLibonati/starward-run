import logging

import pytest

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    @pytest.mark.unit
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test-returns-instance")
        assert isinstance(logger, logging.Logger)

    @pytest.mark.unit
    def test_default_name_is_pygame_app(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "pygame-app"

    @pytest.mark.unit
    def test_custom_name(self) -> None:
        logger: logging.Logger = setup_logger("my-custom-logger")
        assert logger.name == "my-custom-logger"

    @pytest.mark.unit
    def test_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("test-level-debug")
        assert logger.level == logging.DEBUG

    @pytest.mark.unit
    def test_has_at_least_one_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-has-handler")
        assert len(logger.handlers) >= 1

    @pytest.mark.unit
    def test_handler_is_stream_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-stream-handler")
        has_stream: bool = any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
        assert has_stream

    @pytest.mark.unit
    def test_does_not_duplicate_handlers_on_second_call(self) -> None:
        logger: logging.Logger = setup_logger("test-idempotent-handlers")
        count_first: int = len(logger.handlers)
        setup_logger("test-idempotent-handlers")
        assert len(logger.handlers) == count_first

    @pytest.mark.unit
    def test_formatter_includes_levelname(self) -> None:
        logger: logging.Logger = setup_logger("test-formatter")
        handler: logging.Handler = logger.handlers[0]
        assert handler.formatter is not None
        assert "%(levelname)s" in handler.formatter._fmt
