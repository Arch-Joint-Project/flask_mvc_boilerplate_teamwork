from .endpoints.product import product
from .endpoints.user import user


def init_app(app):
    app.register_blueprint(user, url_prefix="/api/users")
    app.register_blueprint(product, url_prefix="/api/products")
