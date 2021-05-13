from app.definitions.factory import Seeder
from app.models import Client


class ClientFactory(Seeder):

    @classmethod
    def run(cls):
        product = Client(
            name=cls.fake.name(),
            age=50
        )
        product.save()
