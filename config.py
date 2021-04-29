import os
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)


class Config:
    """Set Flask configuration vars from .env file."""

    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER = ""

    # General
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "SECRET"
    FLASK_RUN_PORT = 6000

    # Database
    @property
    def SQLALCHEMY_DATABASE_URI(self): # noqa
        return "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
            user=self.DB_USER, pw=self.DB_PASSWORD, url=self.DB_SERVER, db=self.DB_NAME
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_SERVER = os.getenv("DEV_DB_SERVER")


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    DB_SERVER = os.getenv("DB_SERVER")


class TestingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DB_SERVER = os.getenv("DEV_DB_SERVER")
