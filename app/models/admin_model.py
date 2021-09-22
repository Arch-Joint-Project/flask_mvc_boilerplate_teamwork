# local import
from app import db
from .lawyer_model import LawyerModel

# builtin imports
from dataclasses import dataclass

# third party imports
from werkzeug.security import generate_password_hash, check_password_hash


lawyer_model = LawyerModel()
lawyer_obj = lawyer_model.__class__.__name__


@dataclass
class AdminModel(db.Model):
    """
    Table schema for recording admin info
    """
    id: int
    name: str
    username: str
    email: str
    hash_password: str

    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    username = db.Column('username', db.String, nullable=False, unique=True)
    email = db.Column('Email', db.String, nullable=False, unique=True)
    hash_password = db.Column('Password', db.String, nullable=False)
    # forming relationship with the lawyer table using
    # through the lawyer model
    lawyer = db.relationship(lawyer_obj, backref='admin', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("password inaccessible")
        # return self.hash_password

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password, method="sha256")

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)
