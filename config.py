import os
import sys
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Set Flask configuration vars from .env file."""

    DB_ENGINE = "postgres"  # also this can be change from postgres to mongodb

    # SQL database
    DB_SERVER = ""
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    FLASK_ENV = os.getenv("FLASK_ENV")

    # MONGO database
    MONGO_DB = DB_NAME
    MONGODB_PORT = os.getenv("DB_PORT", default=27017)
    MONGODB_USERNAME = DB_USER
    MONGODB_PASSWORD = DB_PASSWORD

    # REDIS
    REDIS_SERVER = os.getenv("REDIS_SERVER")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
    # General
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "SECRET"
    FLASK_RUN_PORT = 6000
    TESTING = False
    LOGFILE = "log.log"

    # Database
    @property
    def MONGODB_HOST(self):  # noqa
        return self.DB_SERVER

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
            user=self.DB_USER,
            pw=self.DB_PASSWORD,
            url=self.DB_SERVER,
            db=self.DB_NAME,
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_SERVER = os.getenv("DEV_DB_SERVER")
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    DB_SERVER = os.getenv("DB_SERVER")
    LOG_BACKTRACE = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    DB_NAME = os.getenv("TEST_DB_NAME")
    MONGODB_HOST = "mongomock://localhost"
    MONGODB_DB = os.getenv("MONGODB_DB")
    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, DB_NAME) + ".sqlite3"
