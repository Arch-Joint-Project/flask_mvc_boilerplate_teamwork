import os
import sys
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Set Flask configuration vars from .env file."""

    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    FLASK_ENV = os.getenv("FLASK_ENV")

    DB_SERVER = ""

    # General
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "SECRET"
    FLASK_RUN_PORT = 6000
    TESTING = False
    LOGFILE = "log.log"

    # Database
    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        if self.FLASK_ENV == "testing":
            return "sqlite:///" + os.path.join(basedir, "test.sqlite")
        else:
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
    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"
    # SQL_ALCHEMY_DATABASE_URI = "sqlite:///:memory:"
