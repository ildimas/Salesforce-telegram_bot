from bot_instance import bot
from routes.reg_route import reg_router
from routes.main_route import main_router
from routes.change_user_info_route import edit_router
from routes.admin_route import admin_router
from services.commands import set_bot_commands
import asyncio
import logging
import sys

from aiogram import Dispatcher
dp = Dispatcher()
dp.include_router(reg_router)
dp.include_router(edit_router)
dp.include_router(admin_router)

async def main() -> None:
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())