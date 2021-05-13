from app.definitions.factory import Seeder
from app.models import Product


class ProductFactory(Seeder):

    @classmethod
    def run(cls):
        product = Product(
            name="bread",
            price=50,
            seller=cls.fake.name()
        )
        product.save()
