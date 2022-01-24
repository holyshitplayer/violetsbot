from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import main_keyboard
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет! Я могу помочь найти любую фиалку, создать документ из данных таблицы и ещё много крутого 😎", reply_markup=main_keyboard)
