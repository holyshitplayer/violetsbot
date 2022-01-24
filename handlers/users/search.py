from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default import main_keyboard
from loader import dp, db
from utils.misc.search_result import search_result_string


@dp.message_handler(text="🔍 Начать поиск")
async def start_search(message: types.Message, state: FSMContext):
    cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Завершить поиск")]], resize_keyboard=True)
    await message.answer("🔍 Введите название сорта", reply_markup=cancel_keyboard)
    await state.set_state("search")


@dp.message_handler(text="❌ Завершить поиск", state="search")
async def search(message: types.Message, state: FSMContext):
    await message.answer("Сделать что нибудь ещё? ✨", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(state="search")
async def search(message: types.Message):
    query = message.text
    msgs = search_result_string(db, query)
    for msg in msgs:
        await message.answer(msg)
    await message.answer("🔍 Введите название следующего сорта")
