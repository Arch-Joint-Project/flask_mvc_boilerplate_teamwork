from app.core.result import Result
from app.core.service_result import ServiceResult, handle_result
from app.repositories import BillRepository


class BillController:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def index(self):
        bill = self.bill_repository.index()
        return ServiceResult(Result(bill, 200))

    def create(self, data):
        bill = self.bill_repository.create(data)
        return ServiceResult(Result(bill, 201))

    # def find_by_id(self, bill_id):
    #     bill = self.repository.find_by_id(bill_id)
    #     return ServiceResult(Result(bill, 200))
    #
    # def find_all(self, bill_id):
    #     bill = self.repository.find_all(bill_id)
    #     return ServiceResult(Result(bill, 200))
    #
    # def delete(self, bill_id):
    #     bill = self.repository.delete(bill_id)
    #     return ServiceResult(Result(bill, 204))
    #
    # def update(self, query_info, obj_in):
    #     bill = self.repository.update(query_info, obj_in)
    #     return ServiceResult(Result(bill, 200))
    #
    # def update_by_id(self, obj_id, obj_in):
    #     bill = self.repository.update_by_id(obj_id, obj_in)
    #     return ServiceResult(Result(bill, 200))
    #
    # def generate_invoice(self, company):
    #     data = self.repository.find_all(company)
    #     if data:
    #         company_bills = defaultdict(list)
    #         total_bill_cost = 0
    #         for each_bill in data:
    #             start_time = list(map(int, str(each_bill.start_time).split(':')))
    #             end_time = list(map(int, str(each_bill.end_time).split(':')))
    #             for index in range(len(start_time)):
    #                 if index == 0:
    #                     if end_time[index] == 0:
    #                         hours_worked = 24 - start_time[index]
    #                     else:
    #                         hours_worked = end_time[index] - start_time[index]
    #                 elif index == 1:
    #                     if start_time[index] > end_time[index]:
    #                         minutes_worked = start_time[index] - end_time[index]
    #                     else:
    #                         minutes_worked = end_time[index] - start_time[index]
    #                     time_worked = round(hours_worked + (minutes_worked / 60),
    #                                         2)
    #             total_rate = time_worked * each_bill.billable_rate
    #             total_bill_cost += total_rate
    #             company_bills[each_bill.company].append({
    #                 "Employee ID": each_bill.id,
    #                 "Number Of Hours": time_worked,
    #                 "Unit Price": each_bill.billable_rate,
    #                 "Cost": total_rate,
    #             })
    #         company_bills[company.get("company")].append({"Total": total_bill_cost})
    #         return ServiceResult(Result(company_bills, 200))
    #     else:
    #         return ServiceResult(Result(data, 200))
