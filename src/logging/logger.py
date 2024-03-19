import logging.config
import pathlib

import yaml

from src.utils.consts import SRC_ROOT_PATH

logger = logging.getLogger(__name__)


def setup_logger():
    config_file = pathlib.Path(SRC_ROOT_PATH, "logging_configs/logger-config.yaml")
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)


setup_logger()