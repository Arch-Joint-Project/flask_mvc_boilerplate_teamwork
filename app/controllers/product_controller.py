from app.definitions.repository.product_repository_interface import \
    ProductRepositoryInterfaceInterface
from app.definitions.result import Result
from app.definitions.service_result import ServiceResult


class ProductController:
    def __init__(
        self,
        product_repository: ProductRepositoryInterfaceInterface
    ):
        self.product_repository = product_repository

    def create_product(self, data):
        product = self.product_repository.create(data)
        return ServiceResult(Result(product, status_code=201))

    def get_product(self, product_id):
        product = self.product_repository.find_by_id(product_id)
        return ServiceResult(Result(product, status_code=200))
