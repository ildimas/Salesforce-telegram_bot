from database.db import async_session
from database.models import User, Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create_user(self, name : str, telegramm_id : int, company_id : UUID) -> User:
        new_user = User(
            user_name = name,
            user_telegramm_id = telegramm_id,
            company_id = company_id
        )
        self.db_session.add(new_user)
        try:
            await self.db_session.flush()
        except IntegrityError:
            await self.db_session.rollback()
        return new_user