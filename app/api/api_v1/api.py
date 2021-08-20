from app.api.api_v1.endpoints.bill_view import bill
from app.api.api_v1.endpoints.user_view import user

def init_app(app):
    app.register_blueprint(bill, url_prefix="/api/bills")
    app.register_blueprint(user, url_prefix="/api/users")
