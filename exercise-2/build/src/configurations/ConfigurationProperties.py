class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOGGER = 'development'
    LOG_FILE_PATH = './src/log/pirelli-data-challenge-dev.log'
    CONSOLE_LOG_LEVEL = "DEBUG"
    FILE_LOG_LEVEL = "DEBUG"
    START_TIMESTAMP = "1970-01-01T00:00:01"
    END_TIMESTAMP = "2050-12-31T23:59:59"
    BATCH_REGISTRY_FILE_PATH = "./src/resources/datasets/batch_registry.csv"
    COOKING_METRICS_FILE_PATH = "./src/resources/datasets/cooking_metrics.csv"
    FAULTY_INTERVALS_FILE_PATH = "./src/resources/datasets/faulty_intervals.csv"
    COMBINATION_TO_COMPUTE = {
        "k": ["k1"],
        "k1": ["m1"],
        "m1": ["a1"]
    }


class LocalTestingConfig(BaseConfig):
    DEBUG = True
    LOGGER = 'local'
    LOG_FILE_PATH = './src/log/pirelli-data-challenge-local.log'
    CONSOLE_LOG_LEVEL = "DEBUG"
    FILE_LOG_LEVEL = "INFO"
    START_TIMESTAMP = "1970-01-01T00:00:01"
    END_TIMESTAMP = "2050-12-31T23:59:59"
    BATCH_REGISTRY_FILE_PATH = "./src/resources/datasets/batch_registry.csv"
    COOKING_METRICS_FILE_PATH = "./src/resources/datasets/cooking_metrics.csv"
    FAULTY_INTERVALS_FILE_PATH = "./src/resources/datasets/faulty_intervals.csv"
    COMBINATION_TO_COMPUTE = {
        "k": ["k1"],
        "k1": ["m1"],
        "m1": ["a1"]
    }
