# local imports
from app.core.repository import SQLBaseRepository
from app.models import AdminModel


class AdminRepository(SQLBaseRepository):
    model=AdminModel
