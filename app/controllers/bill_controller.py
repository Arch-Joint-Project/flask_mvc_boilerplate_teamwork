from flask import jsonify

from app.core.result import Result
from app.core.service_result import ServiceResult
from app.repositories import BillRepository
from collections import defaultdict
from app.utils import create_time_object, create_date_object


class BillController:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def index(self):
        bill = self.bill_repository.index()
        return ServiceResult(Result(bill, 200))

    def create(self, data):
        data["date"] = create_date_object(data["date"])
        data["start_time"] = create_time_object(data["start_time"])
        data["end_time"] = create_time_object(data["end_time"])
        bill = self.bill_repository.create(data)
        return ServiceResult(Result(bill, 201))

    # def find(self, query_params):
    #     bill = self.bill_repository.find(query_params)
    #     return ServiceResult(Result(bill, 200))

    def find_by_id(self, obj_id):
        bill = self.bill_repository.find_by_id(obj_id)
        return ServiceResult(Result(bill, 200))

    def find_all(self, obj_id):
        bill = self.bill_repository.find_all(obj_id)
        return ServiceResult(Result(bill, 200))

    def delete(self, obj_id, user_id):
        bill_info = self.bill_repository.find({"id": obj_id, "lawyer_id": user_id})
        if bill_info:
            bill = self.bill_repository.delete(obj_id)
            return ServiceResult(Result(bill, 204))

    def update_by_id(self, obj_id, obj_in, user_id):
        bill = self.bill_repository.find(
            {"id": obj_id, "lawyer_id": user_id})
        if bill:
            obj_in["date"] = create_date_object(obj_in["date"])
            obj_in["start_time"] = create_time_object(obj_in["start_time"])
            obj_in["end_time"] = create_time_object(obj_in["end_time"])
            bill = self.bill_repository.update_by_id(obj_id, obj_in)
        return ServiceResult(Result(bill, 200))

    def generate_invoice(self, company):
        data = self.bill_repository.find_all(company)
        if data:
            company_bills = defaultdict(list)
            total_bill_cost = 0
            for each_bill in data:
                start_time = list(map(int, str(each_bill.start_time).split(':')))
                end_time = list(map(int, str(each_bill.end_time).split(':')))
                for index in range(len(start_time)):
                    if index == 0:
                        if end_time[index] == 0:
                            hours_worked = 24 - start_time[index]
                        else:
                            hours_worked = end_time[index] - start_time[index]
                    elif index == 1:
                        if start_time[index] > end_time[index]:
                            minutes_worked = start_time[index] - end_time[index]
                        else:
                            minutes_worked = end_time[index] - start_time[index]
                        time_worked = round(hours_worked + (minutes_worked / 60),
                                            2)
                total_rate = time_worked * each_bill.billable_rate
                total_bill_cost += total_rate
                company_bills[each_bill.company].append({
                    "Employee ID": each_bill.id,
                    "Number Of Hours": time_worked,
                    "Unit Price": each_bill.billable_rate,
                    "Cost": total_rate,
                })
            company_bills[company.get("company")].append({"Total": total_bill_cost})
            return ServiceResult(Result(company_bills, 200))
        else:
            return ServiceResult(Result(data, 200))
