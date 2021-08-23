from app.api.api_v1.endpoints.bill_view import bill
from app.api.api_v1.endpoints.user_view import user
from app.api.api_v1.endpoints.account_view import account


def init_app(app):
    app.register_blueprint(bill, url_prefix="/api/bills")
    app.register_blueprint(account, url_prefix="/api/accounts")
    app.register_blueprint(user, url_prefix="/api/users")
