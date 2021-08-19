# local imports
from app.definitions.repository import SQLBaseRepository
from app.models import BillableHourModel


class BillRepository(SQLBaseRepository):
    model=BillableHourModel