# local import
from app import db
from .bill_model import BillModel

# builtin imports
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash


bill_model = BillModel()
bill_obj = bill_model.__class__.__name__


@dataclass
class LawyerModel(db.Model):
    """
    Table schema for recording bills
    """
    id: int
    admin_id: int
    name: str
    username: str
    email: str
    hash_password: str
    bill: db.Model

    __tablename__ = 'lawyers'
    id = db.Column(db.Integer, primary_key=True)
    # foreign key to link this table to the admin table
    # using the admin id
    admin_id = db.Column('Admin ID', db.ForeignKey('admins.id'), nullable=False, index=True)
    name = db.Column('Name', db.String, nullable=False)
    username = db.Column('Username', db.String, nullable=False, unique=True, index=True)
    email = db.Column('Email', db.String, nullable=False, unique=True, index=True)
    hash_password = db.Column('Password', db.String, nullable=False)
    # forming relationship with the bill table
    # through the bill model
    bill = db.relationship(bill_obj, backref='lawyer', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("password is inaccessible")

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password, method="sha256")

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)
