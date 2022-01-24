from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

update_db_keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text="Детки", callback_data="update_kids"),
        InlineKeyboardButton(text="Стартёры", callback_data="update_starters"),
        InlineKeyboardButton(text="Заказы", callback_data="update_orders"),
    ],
    [
        InlineKeyboardButton(text="Все таблицы", callback_data="update_all_db")
    ]
])
