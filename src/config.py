import logging.config
import os

import boto3
from decouple import config  # type: ignore

from src.common.utils.singleton import Singleton


class Config(metaclass=Singleton):
    DATABASE_URL = config("DATABASE_URL", default="postgresql://postgres:postgres@localhost:5432/postgres",cast=str)
    MONGO_DATABASE = "payment"
    MONGODB_URI = config("MONGODB_URI", default="MONGODB_URI=mongodb://user:pass@localhost:27017",cast=str)
    LOG_LEVEL = config("LOG_LEVEL", default="INFO", cast=str)
    TITLE = "FastAPI Clean Architecture"
    VERSION: str = "0.1.0"
    OPENAPI_URL: str = "/openapi.json"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    ROOT_PATH: str = "/"


class DevelopmentConfig(Config):
    LOG_LEVEL = config("LOG_LEVEL", default="DEBUG", cast=str)


class StagingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


def config_factory(environment: str) -> type[Config]:
    configs = {
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
    }
    return configs[environment]


def get_config() -> type[Config]:
    environment = os.getenv("ENVIRONMENT", "development")
    app_config = config_factory(environment)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": (
                    "[%(asctime)s] %(levelname)s "
                    "[%(name)s.%(funcName)s:%(lineno)d] "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%s",
            }
        },
        "handlers": {
            "stdout_logger": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "": {  # root
                "level": app_config.LOG_LEVEL,
                "handlers": ["stdout_logger"],
                "propagate": False,
            }
        },
    }
    logging.config.dictConfig(LOGGING)
    return app_config


class AWSConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.access_key = os.getenv('AWS_ACCESS_KEY_ID')
            cls._instance.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            cls._instance.aws_session_token = os.getenv('AWS_SESSION_TOKEN')
            cls._instance.region = os.getenv('AWS_REGION')
        return cls._instance

    def __get_aws_session(self):
        return boto3.Session(aws_access_key_id=self.access_key,
                             aws_secret_access_key=self.secret_key,
                             aws_session_token=self.aws_session_token,
                             region_name=self.region)

    @staticmethod
    def create_resource(resource: str):
        session = AWSConfig().__get_aws_session()

        return session.client(resource)
