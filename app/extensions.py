from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from app.utils import GUID
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
# jwt = JWTManager()
db.__setattr__("GUID", GUID)
