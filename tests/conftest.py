import pytest
from datetime import date, time
from app.repositories import AdminRepository


@pytest.fixture(scope="class")
def base_test_case_setup_requirement(request):
    request.cls.init_admin_info = {
        "name": "initial_admin",
        "username": "initial_admin_username",
        "email": "initial_admin_email",
        "password": "initial_admin_password"
    }
    request.cls.init_lawyer_info = {
        "admin_id": 1,
        "name": "initial_lawyer",
        "username": "initial_lawyer_username",
        "email": "initial_lawyer_email",
        "password": "initial_lawyer_password"
    }
    request.cls.init_bill_info = {
        "lawyer_id": 1,
        "billable_rate": 300,
        "company": "initial_company",
        "date": date(2020, 1, 4),
        "start_time": time(8, 0),
        "end_time": time(20, 0)
    }
