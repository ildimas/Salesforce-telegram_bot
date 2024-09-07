from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder

# auth_accept_keyboard = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Да'), KeyboardButton(text='Нет')],
#     [KeyboardButton(text='Изменить имя пользователя')]
# ], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

auth_accept_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='name_accept'), InlineKeyboardButton(text='Нет', callback_data='name_decline')]])


main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Зарегистрировать тикет')]], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

admin_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Зарегистрировать компанию"), KeyboardButton(text="Удалить компанию")],
    [KeyboardButton(text="Удалить тикет"), KeyboardButton(text="Удалить пользователя")],
    [KeyboardButton(text = "Вернуться в режим обычного пользователя")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

admin_skip_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Пропустить")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

#! Builder keyboards
companies = ["Подшипник трейд", "Ayeps", "Sony", "Microsoft"]
async def inline_companies():
    keyboard = InlineKeyboardBuilder()
    for company in companies:
        keyboard.add(InlineKeyboardButton(text=company, callback_data=f'company_{company}'))
    return keyboard.adjust(2).as_markup()

