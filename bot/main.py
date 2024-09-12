from bot_instance import bot
from routes.reg_route import reg_router
from routes.ticket_route import ticket_router
from routes.change_user_info_route import edit_router
from routes.admin_route import admin_router
from services.commands import set_bot_commands
import asyncio
import logging
import sys
from web.fastapi import app
from uvicorn import Config, Server

from aiogram import Dispatcher
dp = Dispatcher()
dp.include_router(reg_router)
dp.include_router(edit_router)
dp.include_router(admin_router)
dp.include_router(ticket_router)


async def run_fastapi():
    config = Config(app=app, host="0.0.0.0", port=8000, loop="asyncio")
    server = Server(config=config)
    await server.serve()


async def start_aiogram():
    await set_bot_commands(bot)
    await dp.start_polling(bot)
    
async def main():
    await asyncio.gather(
        run_fastapi(),  # запуск web сервера и aiogramm совместно
        start_aiogram()  
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())