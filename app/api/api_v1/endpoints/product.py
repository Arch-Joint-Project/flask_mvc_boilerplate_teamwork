import pinject
from flask import Blueprint, request

from app.controllers.product_controller import ProductController
from app.controllers.user_controller import UserController
from app.definitions.service_result import handle_result
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository

from app.services.keycloak_service import AuthService
from app.services.redis_service import RedisService
from app.utils.validator import validator

product = Blueprint("product", __name__)

obj_graph = pinject.new_object_graph(
    modules=None, classes=[ProductController, ProductRepository, RedisService]
)

product_controller = obj_graph.provide(ProductController)


@validator()
@product.route("/", methods=["POST"])
def index():
    data = request.json
    result = product_controller.create_product(data)
    return handle_result(result)
