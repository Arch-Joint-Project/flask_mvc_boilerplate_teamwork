# local import
from app import db
from .lawyer_model import LawyerModel
# builtin imports
from dataclasses import dataclass


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
    password: str
    lawyer: db.Model

    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.Integer, nullable=False)
    username = db.Column('username', db.String, nullable=False, unique=True)
    email = db.Column('Email', db.String, nullable=False, unique=True)
    password = db.Column('Password', db.String, nullable=False)
    # forming relationship with the lawyer table using
    # through the lawyer model
    lawyer = db.relationship(lawyer_obj, backref='admin', lazy='dynamic')

