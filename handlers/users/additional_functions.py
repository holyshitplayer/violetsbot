from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline import additional_functions_keyboard, update_db_keyboard
from loader import dp, db


@dp.message_handler(text="⚙ Дополнительные возможности")
async def additional_functions(message: types.Message):
    await message.answer(text="Выберите одну из предложенных функций", reply_markup=additional_functions_keyboard)


@dp.callback_query_handler(text="update_db")
async def choose_db_to_update(call: CallbackQuery):
    await call.message.edit_text(text="Выберите таблицу которую нужно обновить", reply_markup=update_db_keyboard)


@dp.callback_query_handler(text="total_in_stock")
async def total_in_stock(call: CallbackQuery):
    in_kids = db.count_kids()
    in_starters = db.count_starters()
    in_orders = db.count_orders()
    await call.message.edit_text(text=f"Всего в таблице деток - <b>{in_kids}</b> шт.\n"
                                      f"Всего в таблице стартёров - <b>{in_starters}</b> шт.\n"
                                      f"Всего в таблице заказов - <b>{in_orders}</b> шт.")


@dp.callback_query_handler(text="total_in_collection")
async def total_in_collection(call: CallbackQuery):
    in_collection = db.count_sorts()
    await call.message.edit_text(text=f"Всего в коллекции - <b>{in_collection}</b> сортов.")
