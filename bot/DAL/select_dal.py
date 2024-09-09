from database.db import async_session
from database.models import User, Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

class SelectDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def get_all_companies(self) -> List[Company]:
        query = select(Company)
        result = await self.db_session.execute(query)
        companies = result.scalars().all()
        return companies
    
    async def get_all_users(self) -> List[User]:
        query = select(User)
        result = await self.db_session.execute(query)
        users = result.scalars().all()
        return users
    
    async def get_user_by_telegramm_id(self, telegram_id : int) -> User:
        query = select(User).where(User.user_telegramm_id == telegram_id)
        result = await self.db_session.execute(query)
        user = result.fetchone()
        return user
    
    async def get_company_by_id(self, id : str) -> Company:
        query = select(Company).where(Company.company_id == id)
        result = await self.db_session.execute(query)
        company = result.fetchone()
        return company