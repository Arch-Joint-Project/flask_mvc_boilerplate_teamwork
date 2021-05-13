from app.definitions.factory import Seeder
from app.models.user import User


class UserFactory(Seeder):

    @classmethod
    def run(cls):
        user = User(
            name=cls.fake.name(),
            email=cls.fake.email()
        )

        cls.db.session.add(user)
        cls.db.session.commit()
