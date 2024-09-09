from database.db import async_session
from database.models import User, Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

class RegDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def get_all_companies(self) -> List[Company]:
        query = select(Company)
        result = await self.db_session.execute(query)
        categories = result.scalars().all()
        return categories