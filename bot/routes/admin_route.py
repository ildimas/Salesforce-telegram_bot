from aiogram.filters import Command
from aiogram import Router, types, F
from services.fsm import Admin, MainUsage
from aiogram.fsm.context import FSMContext
import services.keyboards as keyboard
from DAL.admin_dal import AdminDAL
from services.hashing import Hasher
from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generator
import os
from services.salesforce_connect import *
from dotenv import load_dotenv
load_dotenv()

        
admin_router = Router()
hasher = Hasher()

#! commands
@admin_router.message(Command('admin'))
async def admin_auth(msg: types.Message, state : FSMContext) -> None:
    await msg.answer(f'Введите ваш ключ доступа:')
    await state.set_state(Admin.admin_verifying_key)
    
#! Handlers

@admin_router.message(Admin.admin_verifying_key)
async def admin_verifying(msg: types.Message, state: FSMContext) -> None:
    if msg.text == os.getenv("ADMIN_KEY"):
        await state.set_state(Admin.admin_acsess)
        await msg.answer("Вам выдан статус администратора. Используйте меню снизу для управления", reply_markup=keyboard.admin_menu_keyboard)
        await msg.delete()
    else:
        await msg.answer("Неверно введенный ключ")
        await msg.delete()
      
@admin_router.message(F.text == "Зарегистрировать компанию", Admin.admin_acsess)
async def admin_create_org(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(Admin.admin_company_creation_name)
    await msg.answer("Введите название комании (Обязательно):")
    
@admin_router.message(F.text == "Удалить компанию", Admin.admin_acsess)
async def admin_delete_org(msg: types.Message, state: FSMContext) -> None:
    pass
    
@admin_router.message(F.text == "Удалить тикет", Admin.admin_acsess)
async def admin_delete_ticket(msg: types.Message, state: FSMContext) -> None:
    pass
    
@admin_router.message(F.text == "Удалить пользователя", Admin.admin_acsess)
async def admin_delete_user(msg: types.Message, state: FSMContext) -> None:
    pass

@admin_router.message(F.text == "Вернуться в режим обычного пользователя", Admin.admin_acsess)
async def admin_delete_user(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MainUsage.ticket_acsess)
    await msg.answer("Создайте тикет:", reply_markup=keyboard.main_menu_keyboard)


#! cc handlers
@admin_router.message(Admin.admin_company_creation_name)
async def admin_creating_org_name(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(admin_company_creation_name = msg.text)
    await state.set_state(Admin.admin_company_creation_password)
    await msg.answer("Введите пароль для компании (Обязательно):")
    
@admin_router.message(Admin.admin_company_creation_password)
async def admin_creating_org_password(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(admin_company_creation_password = msg.text)
    await msg.delete()
    await state.set_state(Admin.admin_company_creation_email)
    await msg.answer("Введите адресс электронной почты компании (Опционально):", reply_markup=keyboard.admin_skip_keyboard)
    
@admin_router.message(Admin.admin_company_creation_email)
async def admin_creating_org_email(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(Admin.admin_company_creation_phone)
    if msg.text != "Пропустить":
        await state.update_data(admin_company_creation_email = msg.text)
    await msg.answer("Введите телефон компании (Опционально):", reply_markup=keyboard.admin_skip_keyboard)
    
@admin_router.message(Admin.admin_company_creation_phone)
async def admin_creating_org_website(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(Admin.admin_company_creation_website)
    if msg.text != "Пропустить":
        await state.update_data(admin_company_creation_phone = msg.text)
    await msg.answer("Введите адресс вебсайта компании (Опционально):", reply_markup=keyboard.admin_skip_keyboard)
    
@admin_router.message(Admin.admin_company_creation_website)
async def admin_creating_org_additionalinfo(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(Admin.admin_company_creation_additional_info)
    if msg.text != "Пропустить":
        await state.update_data(admin_company_creation_website = msg.text)
    await msg.answer("Введите дополнительную ифнормацию о компании (Опционально):", reply_markup=keyboard.admin_skip_keyboard)
    
@admin_router.message(Admin.admin_company_creation_additional_info)
async def admin_creating_org_final(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(Admin.admin_acsess)
    if msg.text != "Пропустить":
        await state.update_data(admin_company_creation_additional_info = msg.text)
    data = await state.get_data()
    get_value = lambda d, key: d[key] if key in d else "-"
    
    name = get_value(data, 'admin_company_creation_name')
    
    #! Sf operations
    sf_id = await sf_company_create(company_name=name)
    # sf_id = await sf_findout_comp_id(company_name=name)
    
    async for db_session in get_db():
        
        adm_dal = AdminDAL(db_session)
        
        await adm_dal.create_company(name,
                                    password := hasher.get_password_hash(get_value(data, 'admin_company_creation_password')),
                                    phone := get_value(data, 'admin_company_creation_phone'),
                                    email := get_value(data, 'admin_company_creation_email'),
                                    add_info := get_value(data, 'admin_company_creation_additional_info'),
                                    website := get_value(data, 'admin_company_creation_website'),
                                    sf_id = sf_id
                                    )
        
    message_text = (
            f"Вы успешно закончили процесс создания команды.\n\n"
            f"Данные:\n"
            f"Название: <b>{name}</b>\n"
            f"Url: <b>{website}</b>\n"
            f"Email: <b>{email}</b>\n"
            f"Телефон: <b>{phone}</b>\n"
            f"id salesforce: <b>{sf_id}</b>\n"
            f"Дополнительная информация: <b>{add_info}</b>\n\n"
            f"Дальнейшие манипуляции вы можете совершать с помощью меню снизу:" 
        )
    await msg.answer(message_text, reply_markup=keyboard.admin_menu_keyboard)

#! callback querries 


#! functions