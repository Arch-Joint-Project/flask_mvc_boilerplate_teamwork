from app.definitions.result import Result
from app.definitions.service_result import ServiceResult
from app.repositories import BillRepository


class BillController:
    def __init__(self, bill_repository: BillRepository):
        self.repository = bill_repository

    def index(self):
        bill = self.repository.index()
        return ServiceResult(Result(bill, 200))

    def create(self, data):  # data is coming from the view
        bill = self.repository.create(data)
        return bill

    def find_by_id(self, bill_id):
        bill = self.repository.find_by_id(bill_id)
        return bill

    def find_all(self, bill_id):
        bill = self.repository.find_all(bill_id)
        return bill

    def delete(self, bill_id):
        bill = self.repository.delete(bill_id)
        return bill

    def update(self, query_info, obj_in):
        bill = self.repository.update(query_info, obj_in)
        return bill

    def update_by_id(self, obj_id, obj_in):
        bill = self.repository.update_by_id(obj_id, obj_in)
        return bill
