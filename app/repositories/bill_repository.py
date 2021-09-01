# local imports
from app.core.repository import SQLBaseRepository
from app.models import BillModel


class BillRepository(SQLBaseRepository):
    model=BillModel
