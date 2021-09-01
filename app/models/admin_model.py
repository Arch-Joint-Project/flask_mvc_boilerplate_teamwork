# local import
from app import db
from app.models import LawyerModel

# builtin imports
from dataclasses import dataclass
from datetime import date, time

lawyer_model = LawyerModel()


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

    __tablename__ = 'admin'
    id = db.Column('Admin ID', db.Integer, primary_key=True, nullable=False)
    name = db.Column('Name', db.Integer, nullable=False)
    username = db.Column('username', db.String, nullable=False, unique=True)
    email = db.Column('Email', db.String, nullable=False, unique=True)
    password = db.Column('Password', db.String, nullable=False)
    lawyer = db.relationship(lawyer_model, back_ref='admin', lazy='dynamic')

