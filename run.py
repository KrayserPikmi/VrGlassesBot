import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
load_dotenv()

from app.heandlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())