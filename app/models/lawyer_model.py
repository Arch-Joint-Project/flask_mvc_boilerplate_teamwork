# local import
from app import db
from app.models import AdminModel
# builtin imports
from dataclasses import dataclass
from datetime import date, time

admin_model = AdminModel()

fk = admin_model.__tablename__ + ".id"

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
    password: str

    __tablename__ = 'lawyers'
    id = db.Column('Employee ID', db.Integer, primary_key=True, nullable=False)
    admin_id = db.Column('Admin ID', db.ForeignKey(admin_model), nullable=False)
    name = db.Column('Name', db.String(60), primary_key=True, nullable=False)
    username = db.Column('Username', db.String, nullable=False)
    email = db.Column('Email', db.String, nullable=False)
    password = db.Column('Password', db.String, nullable=False)
