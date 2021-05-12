from dataclasses import dataclass
import mongoengine as me

from app import db


@dataclass
class User(db.Model):
    _id: int
    email: str
    name: str
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    name = db.Column(db.String(60), nullable=False)



class Product(me.Document):
    name = me.StringField(max_length=60, required=True)
    price = me.IntField(required=True)
    seller = me.StringField(required=True)


