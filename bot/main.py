from bot_instance import bot
from routes.user_route import user_router

import asyncio
import logging
import sys

from aiogram import Dispatcher
dp = Dispatcher()
dp.include_router(user_router) 


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())