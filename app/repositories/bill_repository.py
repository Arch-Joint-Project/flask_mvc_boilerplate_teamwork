# local imports
from app.core.repository import SQLBaseRepository
from app.models import BillModel


class BillRepository(SQLBaseRepository):
    model = BillModel

    def __init__(self):
        super(BillRepository,self).__init__()

    def delete(self, query_params):
        bill_info = super(BillRepository, self).find(query_params)
        bill = super(BillRepository, self).delete(bill_info.id)
        print('this is bill', bill)
        return bill

