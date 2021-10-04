from app.models import AdminModel, LawyerModel, BillModel
from datetime import date, time


def setup_data():
    admin = {
        "name": "test_admin",
        "username": "test_admin_username",
        "email": "test_admin_email",
        "password": "test_admin_password"
    }
    lawyer = {
        "admin_id": 1,
        "name": "test_lawyer",
        "username": "test_lawyer_username",
        "email": "test_lawyer_email",
        "password": "test_lawyer_password"
    }
    bill = {
        "lawyer_id": 1,
        "billable_rate": 300,
        "company": "initial_company",
        "date": date(2020, 1, 4),
        "start_time": time(8, 0),
        "end_time": time(20, 0)
    }
    return admin, lawyer, bill


def model_data():
    admin_data, lawyer_data, bill_data = setup_data()
    admin = AdminModel(**admin_data)
    lawyer = LawyerModel(**lawyer_data)
    bill = BillModel(**bill_data)
    return admin, lawyer, bill

