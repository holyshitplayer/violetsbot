import logging

from aiogram.types import CallbackQuery

from loader import dp, db
from utils.misc.export_excel_data import sorts_values_from_excel, content_values_from_excel
from utils.misc.load_xlsx_sheet import load_kids_sheet, load_starters_sheet, load_orders_sheet


@dp.callback_query_handler(text="update_kids")
async def update_kids_db(call: CallbackQuery):
    try:
        db.refill_table_kids(content_values_from_excel(db, load_kids_sheet()))
    except Exception as err:
        logging.info(f"Error while updating table kids:\n{err}")
    logging.info(f"Updated table kids")
    await call.message.edit_text(text="Вы обновили таблицу деток!")


@dp.callback_query_handler(text="update_starters")
async def update_starters_db(call: CallbackQuery):
    try:
        db.refill_table_starters(content_values_from_excel(db, load_starters_sheet()))
    except Exception as err:
        logging.info(f"Error while updating table starters:\n{err}")
    logging.info(f"Updated table starters")
    await call.message.edit_text(text="Вы обновили таблицу стартёров!")


@dp.callback_query_handler(text="update_orders")
async def update_orders_db(call: CallbackQuery):
    try:
        db.refill_table_orders(content_values_from_excel(db, load_orders_sheet()))
    except Exception as err:
        logging.info(f"Error while updating table orders:\n{err}")
    logging.info(f"Updated table orders")
    await call.message.edit_text(text="Вы обновили таблицу заказов!")


@dp.callback_query_handler(text="update_all_db")
async def update_all_db(call: CallbackQuery):
    try:
        db.refill_table_sorts(sorts_values_from_excel())
        db.refill_table_kids(content_values_from_excel(db, load_kids_sheet()))
        db.refill_table_starters(content_values_from_excel(db, load_starters_sheet()))
        db.refill_table_orders(content_values_from_excel(db, load_orders_sheet()))
    except Exception as err:
        logging.info(f"Error while updating all tables:\n{err}")
    logging.info(f"Updated all tables")
    await call.message.edit_text(text="Вы обновили все таблицы!")
