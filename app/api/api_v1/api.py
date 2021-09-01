from app.api.api_v1.endpoints import admin
from app.api.api_v1.endpoints import lawyer
from app.api.api_v1.endpoints import bill


def init_app(app):
    """
    Register app blueprints over here
    eg: # app.register_blueprint(user, url_prefix="/api/users")
    :param app:
    :return:
    """
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(lawyer, url_prefix="/lawyer")
    app.register_blueprint(bill, url_prefix="/bill")
