# # local import
# from app import db
#
# # builtin imports
# from dataclasses import dataclass
# from datetime import date, time
#
#
# @dataclass
# class BillModel(db.Model):
#     """
#     Table schema for recording bills
#     """
#     id: int
#     lawyer_id: int
#     billable_rate: int
#     company: str
#     date: date
#     start_time: time
#     end_time: time
#
#     __tablename__ = 'bills'
#     id = db.Column(db.Integer, primary_key=True)
#     # foreign key to link this table to the lawyers table using
#     # the lawyers id
      lawyer_id = db.Column('Lawyer ID', db.ForeignKey('lawyers.id'), index=True, nullable=False)
#     billable_rate = db.Column('Billable Rate (per hour)', db.Integer, nullable=False)
#     company = db.Column('Company', db.String, nullable=False, index=True)
#     date = db.Column('Date', db.Date, nullable=False)
#     start_time = db.Column('Start Time', db.Time, nullable=False)
#     end_time = db.Column('End Time', db.Time, nullable=False)
