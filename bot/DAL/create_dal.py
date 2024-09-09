from database.db import async_session
from database.models import User, Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List
from sqlalchemy import select

class CreateDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create_user(self, name : str, telegramm_id : int, company_id : UUID, sf_id : str) -> User:
        new_user = User(
            user_name = name,
            user_telegramm_id = telegramm_id,
            company_id = company_id,
            user_sf_id =  sf_id
        )
        self.db_session.add(new_user)
        try:
            await self.db_session.flush()
        except IntegrityError:
            await self.db_session.rollback()
        return new_user
    
    async def create_company(self, name : str, password : str, phone : str, email : str, add_info : str, website : str, sf_id : str) -> Company:
        new_company = Company(company_name=name, 
                              company_hashed_password=password,
                              company_corporeate_mail=email,
                              company_phone=phone,
                              company_website=website,
                              company_additional_info=add_info,
                              company_sf_id = sf_id)
        self.db_session.add(new_company)
        try:
            await self.db_session.flush()
        except IntegrityError:
            await self.db_session.rollback()
        return new_company
    
    # async def create_ticket(self, )
