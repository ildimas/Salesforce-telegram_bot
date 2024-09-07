from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

async def set_bot_commands(bot : Bot):
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/change_company", description="Изменить организацию"),
        types.BotCommand(command="/change_username", description="Изменить имя пользователя"),
        types.BotCommand(command="/admin", description="Доступ администратора")
    ]
    await bot.set_my_commands(commands)