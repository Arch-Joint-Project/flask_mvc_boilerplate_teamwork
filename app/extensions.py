from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.utils import GUID
from flask_mail import Mail
from celery import Celery
# from app.utils.task.make_celery import make_celery

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
celery = Celery()
# jwt = JWTManager()
db.__setattr__("GUID", GUID)
