import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import setup_dialogs, StartMode, DialogManager

from dialogs.tasks import main_dialog
from settings import Settings
from states import BotStates

logging.basicConfig(level=logging.INFO)

settings = Settings()

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
setup_dialogs(dp)

dp.include_router(main_dialog)


@dp.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotStates.START, mode=StartMode.RESET_STACK)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
