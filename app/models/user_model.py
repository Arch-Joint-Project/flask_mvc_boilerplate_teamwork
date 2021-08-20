# builtin imports
from datetime import date
from dataclasses import dataclass

# local imports
from app import db

# third party imports
from sqlalchemy.dialects.postgresql import UUID


@dataclass
class UserModel(db.Model):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    age: int
    date_of_birth: date
    password: str

    __tablename__ = "users"
    id = db.Column("User ID", db.Integer, primary_key=True)
    first_name = db.Column("First Name", db.String(), nullable=False)
    last_name = db.Column("Last Name", db.String(), nullable=False)
    username = db.Column("Username", db.String(), unique=True, nullable=False)
    email = db.Column("Email", db.String(), unique=True, nullable=False)
    age = db.Column("Age", db.Integer, nullable=False)
    # date_of_birth = db.Column("Date of Birth", db.String, nullable=False)
    date_of_birth = db.Column("Date of Birth", db.Date(), nullable=False)
    # error json is not serializable
    password = db.Column("Password", db.String(), nullable=False)
