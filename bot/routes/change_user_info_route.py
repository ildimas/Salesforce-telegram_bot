from aiogram.filters import Command
from aiogram import Router, types
from services.fsm import Registrarion, MainUsage
from aiogram.fsm.context import FSMContext
import services.keyboards as keyboard
from aiogram.filters import Command

edit_router = Router()


#! commands
@edit_router.message(Command('change_company'))
async def change_company(msg: types.Message, state : FSMContext) -> None:
    await state.set_state(MainUsage.changing_org)
    await msg.answer(f'Выберите вашу компанию:', reply_markup=await keyboard.inline_companies())
    await state.update_data(name = f"{msg.chat.first_name} {msg.chat.last_name}")
    await state.update_data(user_telegram_id = msg.from_user.id)
    
@edit_router.message(Command('change_username'))
async def change_username(msg: types.Message, state : FSMContext) -> None:
    await state.set_state(MainUsage.changing_name)
    await msg.answer(f'Введите ваше новое имя:')  #reply_markup=keyboard.auth_accept_inline_keyboard

    
#! Handlers

@edit_router.message(MainUsage.changing_org)
async def handle_org_change(msg: types.Message, state: FSMContext) -> None:
    #! Check if the password is valid
    data = await state.get_data()
    message_text = message_text = (
            f"Вы успешно сменили вашу организацию на <b>{data['changing_org']}</b>.\n\n"
            f"Дальнейшие манипуляции вы можете совершать с помощью меню снизу:" 
        )
    
    await msg.answer(message_text, reply_markup=keyboard.main_menu_keyboard)
    await state.set_state(MainUsage.ticket_acsess)
        
@edit_router.message(MainUsage.changing_name)
async def handle_username_change(msg: types.Message, state: FSMContext) -> None:
    new_name = msg.text
    await msg.answer(f"Ваше новое имя <b>{new_name}</b>", reply_markup=keyboard.main_menu_keyboard)
    await state.set_state(MainUsage.ticket_acsess)
      
#! callback queries 

@edit_router.callback_query(lambda c: c.data.startswith('company_'), MainUsage.changing_org)
async def company_changing_callback_querry(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    company = callback_query.data.split('_')[-1]
    selected_company = company
    await state.update_data(changing_org=selected_company)
    await callback_query.message.answer("Введите пароль для доступа к вашей организации:")
    