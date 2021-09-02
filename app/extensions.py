from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.utils import GUID
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jw = JWTManager()
db.__setattr__("GUID", GUID)
