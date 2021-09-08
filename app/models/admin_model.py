# local import
from app import db, create_app
from .lawyer_model import LawyerModel
# builtin imports
from dataclasses import dataclass
from flask import request, jsonify
from functools import wraps
import jwt

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

    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String, nullable=False)
    username = db.Column('username', db.String, nullable=False, unique=True)
    email = db.Column('Email', db.String, nullable=False, unique=True)
    password = db.Column('Password', db.String, nullable=False)
    # forming relationship with the lawyer table using
    # through the lawyer model
    lawyer = db.relationship(lawyer_obj, backref='admin', lazy='dynamic')






