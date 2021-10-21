from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.utils import GUID
from flask_mail import Mail
from flask_celeryext import FlaskCeleryExt

from app.utils.task.make_celery import make_celery

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)



# jwt = JWTManager()
db.__setattr__("GUID", GUID)
