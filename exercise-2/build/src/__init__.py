import logging
import os
from datetime import datetime
from src.configurations.ConfigurationProperties import *
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler


def arguments_validation(args):
    check_timestamp_value(args.start_timestamp)
    check_timestamp_value(args.end_timestamp)


def check_timestamp_value(string_datetime):
    try:
        if string_datetime:
            datetime.strptime(string_datetime, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise ValueError("Incorrect data format, inputs should be YYYY-MM-DDTHH:MM:SS")


def create_configurations(args, env='ENV'):
    config_name = os.getenv(env, "development")
    configurations = init_configurations(config_name)
    init_logging(configurations)
    if args.start_timestamp:
        configurations.START_TIMESTAMP = args.start_timestamp
    if args.end_timestamp:
        configurations.END_TIMESTAMP = args.end_timestamp
    logging.info(f"Environment: {config_name}")
    return configurations


def init_configurations(env):
    logging.info(f"Loading configurations for {env}")
    if env.__eq__('development'):
        return DevelopmentConfig
    if env.__eq__('local'):
        return LocalTestingConfig


def init_logging(configurations):
    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - "
                                  "level=%(levelname)s - "
                                  "%(name)s - "
                                  "%(threadName)s - "
                                  "%(message)s")

    handler = TimedRotatingFileHandler(configurations.LOG_FILE_PATH, when='midnight')
    handler.setLevel(configurations.FILE_LOG_LEVEL)
    handler.setFormatter(formatter)
    handler.suffix = '%Y%m%d'
    root_logger.addHandler(handler)

    if not configurations.LOGGER.__eq__('production'):
        console_handler = StreamHandler()
        console_handler.setLevel(configurations.CONSOLE_LOG_LEVEL)
        console_handler.setFormatter(formatter)
        console_handler.suffix = '%Y%m%d'
        root_logger.addHandler(console_handler)
    logging.debug("Logger setup completed")