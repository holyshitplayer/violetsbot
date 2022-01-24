from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

additional_functions_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Всего в наличии", callback_data="total_in_stock"),
        InlineKeyboardButton(text="Всего сортов", callback_data="total_in_collection"),
    ],
    [
        InlineKeyboardButton(text="Обновить БД", callback_data="update_db"),
    ],
])
