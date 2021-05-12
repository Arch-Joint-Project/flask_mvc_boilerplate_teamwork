import pinject
from flask import Blueprint, request

from app.controllers.product_controller import ProductController
from app.controllers.user_controller import UserController
from app.definitions.service_result import handle_result
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schema.product_schema import Product

from app.services.keycloak_service import AuthService
from app.services.redis_service import RedisService
from app.utils.validator import validator

product = Blueprint("product", __name__)

obj_graph = pinject.new_object_graph(
    modules=None, classes=[ProductController, ProductRepository, RedisService]
)

product_controller = obj_graph.provide(ProductController)


@validator(schema=Product())
@product.route("/", methods=["POST"])
def create():
    """
    ---
    post:
      description: creates a new product
      requestBody:
        required: true
        content:
            application/json:
                schema: Product
      responses:
        '201':
          description: call successful
          content:
            application/json:
              schema: Product
      tags:
          - Product
    """
    data = request.json
    result = product_controller.create_product(data)
    return handle_result(result, schema=Product())


@product.route("/<string:product_id>")
def get(product_id):
    """
    ---
    get:
      parameters:
        - in: path
          name: product_id   # Note the name is the same as in the path
          required: true
          schema:
            type: string
          description: The product ID
      responses:
        '200':
          description: returns a product
          content:
            application/json:
              schema: Product
      tags:
          - Product
    """

    result = product_controller.get_product(product_id)
    return handle_result(result, schema=Product())
