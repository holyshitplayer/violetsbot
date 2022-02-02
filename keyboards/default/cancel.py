from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="❌ Отменить")]
    ],
    resize_keyboard=True
)
