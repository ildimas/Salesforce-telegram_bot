from aiogram.filters import Command
from aiogram import Router, types, F
from services.fsm import Registrarion, MainUsage
from aiogram.fsm.context import FSMContext
import services.keyboards as keyboard
from database.db import get_db
from DAL.select_dal import SelectDAL
from services.salesforce_connect import sf_ticket_create

ticket_router = Router()

#! commands

#! Handlers

@ticket_router.message(F.text == "Зарегистрировать тикет", MainUsage.ticket_acsess)
async def ticket_reg(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MainUsage.ticket_creation)
    await msg.answer("Введите название вашего тикета:")

@ticket_router.message(MainUsage.ticket_creation)
async def ticker_create(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MainUsage.ticket_fill)
    async for db_session in get_db():
        dal = SelectDAL(db_session)
        user_obj = await dal.get_user_by_telegramm_id(telegram_id=msg.from_user.id)
        print(user_obj.company_id)
        company_obj = await dal.get_company_by_id(id=user_obj.company_id)
    ticket_sf_id = await sf_ticket_create(ticket_name=msg.text, user_sf_id=user_obj.user_sf_id, company_sf_id=company_obj.company_sf_id)
        
    await msg.answer(f"Тикет создан {ticket_sf_id} - пока все :)")


#! handlers

#! callback querries 

#! functions