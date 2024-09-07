from aiogram.filters import Command
from aiogram import Router, types
from services.fsm import Registrarion, MainUsage
from aiogram.fsm.context import FSMContext
import services.keyboards as keyboard
reg_router = Router()

@reg_router.message(Command('start'))
async def one_start(msg: types.Message, state : FSMContext) -> None:
    await state.set_state(Registrarion.await_base_infromation)
    first_name = msg.chat.first_name
    last_name = msg.chat.last_name or ""
    await msg.answer(f'Добро пожаловать в бота отправки тикетов. Вы будете зарегистрированный в системе как <b>{first_name} {last_name}</b>, Вас устроит такое имя ?', reply_markup=keyboard.auth_accept_inline_keyboard)
    await state.update_data(name = f"{msg.chat.first_name} {msg.chat.last_name}")
    await state.update_data(user_telegram_id = msg.from_user.id)
    
@reg_router.callback_query(lambda c: c.data == 'name_accept', Registrarion.await_base_infromation)
async def two_start(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Registrarion.await_organization)
    await callback_query.answer("Вы успешно зарегистрировали пользователя !") 
    await callback_query.message.answer("Выберите свою организацию из спсика:", reply_markup=await keyboard.inline_companies())
    
@reg_router.callback_query(lambda c: c.data == 'name_decline', Registrarion.await_base_infromation)
async def three_start(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.edit_text("Пожалуйста, введите ваше новое имя:")
    await state.set_state(Registrarion.await_new_name)
    await callback_query.answer()  
    
@reg_router.message(Registrarion.await_new_name)
async def handle_new_name(msg: types.Message, state: FSMContext) -> None:
    new_name = msg.text
    await state.update_data(name=new_name)
    await msg.answer(
        f"Ваше новое имя <b>{new_name}</b>. Вас устраивает такое имя?",
        reply_markup=keyboard.auth_accept_inline_keyboard,
    )
    await state.set_state(Registrarion.await_base_infromation)
    
@reg_router.callback_query(lambda c: c.data.startswith('company_'), Registrarion.await_organization)
async def company_selection(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    company = callback_query.data.split('_')[-1]
    selected_company = company
    await state.update_data(await_organization=selected_company)
    await state.set_state(Registrarion.await_organization_password)
    await callback_query.message.answer("Введите пароль для доступа к вашей организации:")
    
@reg_router.message(Registrarion.await_organization_password)
async def handle_org_password(msg: types.Message, state: FSMContext) -> None:
    #! Check if the password is valid
    data = await state.get_data()
    message_text = message_text = (
            f"Вы успешно закончили процесс авторизации в системе отправки тикетов.\n\n"
            f"Ваши данные:\n"
            f"Имя: <b>{data['name']}</b>\n"
            f"Компания: <b>{data['await_organization']}</b>\n\n"
            f"Дальнейшие манипуляции вы можете совершать с помощью меню снизу:" 
        )
    
    await msg.answer(message_text, reply_markup=keyboard.main_menu_keyboard)
    await state.set_state(MainUsage.ticket_acsess)
    