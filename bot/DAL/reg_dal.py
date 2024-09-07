from ..database.db import async_session
from ..database.models import User, Company
from sqlalchemy.ext.asyncio import AsyncSession

class RefDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create_user(self):
        pass