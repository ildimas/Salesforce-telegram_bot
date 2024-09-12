from aiogram.filters import Command
from aiogram import Router, types, F
from services.fsm import Registrarion, MainUsage
from aiogram.fsm.context import FSMContext
import services.keyboards as keyboard
from database.db import get_db
from DAL.select_dal import SelectDAL
from DAL.create_dal import CreateDAL
from services.salesforce_connect import sf_ticket_create, sf_message_create
import asyncio
from web.fastapi import message_dict

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
        company_obj = await dal.get_company_by_id(id=user_obj.company_id)
    ticket_sf_id = await sf_ticket_create(ticket_name=msg.text, user_sf_id=user_obj.user_sf_id, company_sf_id=company_obj.company_sf_id)
    async for db_session in get_db():
        dal = CreateDAL(db_session)
        await dal.create_ticket(ticket_sf_id=ticket_sf_id, ticket_name=msg.text, company_id=company_obj.company_id, user_id=user_obj.user_id)
    await state.set_state(MainUsage.ticket_processing)
    await state.update_data(ticket_processing=ticket_sf_id)
    await msg.answer(f"Id вашего тикета: {ticket_sf_id} - вы можете пользоваться этим чатом для связи с тех поддержкой. Опишите вашу проблему :)")
    
@ticket_router.message(MainUsage.ticket_processing)
async def ticker_proc(msg: types.Message, state: FSMContext) -> None:
   data = await state.get_data()
   ticket_sf_id = data['ticket_processing']
   body = msg.text
   message_sf_id = await sf_message_create(ticket_sf_id=ticket_sf_id, body=body)
   print(message_sf_id, "Создано")
   print(ticket_sf_id, "айди тикета")
   while True:
        if ticket_sf_id in await message_dict.keys():
            await msg.answer(await message_dict.get(ticket_sf_id))
            await message_dict.delete(ticket_sf_id)
        await asyncio.sleep(5)
        




#! handlers

#! callback querries 

#! functions
            
            