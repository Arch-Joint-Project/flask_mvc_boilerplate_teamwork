from app.api.api_v1.endpoints.bill_view import bill


def init_app(app):
    app.register_blueprint(bill, url_prefix="/api/bills")
