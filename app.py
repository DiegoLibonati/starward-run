import os

from dotenv import load_dotenv

from src.configs.development_config import DevelopmentConfig
from src.configs.logger_config import setup_logger
from src.configs.production_config import ProductionConfig
from src.configs.testing_config import TestingConfig
from src.ui.interface_game import InterfaceGame

logger = setup_logger("game - app.py")

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def main(environment: str = "production") -> None:
    load_dotenv()

    environment = os.getenv("ENVIRONMENT", environment)

    config_class = CONFIG_MAP.get(environment, ProductionConfig)
    config = config_class()

    game = InterfaceGame(config=config)
    game.game_loop()

    logger.info("Game finished: %s", game)


if __name__ == "__main__":
    main(environment="development")
