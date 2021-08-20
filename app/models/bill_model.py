# local import
from app import db

# builtin imports
from dataclasses import dataclass
from datetime import date, time


@dataclass
class BillableHourModel(db.Model):
    """
    Table schema for recording bills
    """
    id: int
    billable_rate: int
    company: str
    date: date
    start_time: time
    end_time: time

    __tablename__ = 'billing_db'
    id = db.Column('Employee ID', db.Integer, primary_key=True, nullable=False)
    billable_rate = db.Column('Billable Rate (per hour)', db.Integer, nullable=False)
    company = db.Column('Company', db.String(60), primary_key=True, nullable=False)
    date = db.Column('Date', db.Date, nullable=False)
    start_time = db.Column('Start Time', db.Time, nullable=False)
    end_time = db.Column('End Time', db.Time, nullable=False)
