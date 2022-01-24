from aiogram import types

from keyboards.default import main_keyboard
from loader import dp


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def echo(message: types.Message):
    await message.answer("Выберите одну из предложенных функций", reply_markup=main_keyboard)
