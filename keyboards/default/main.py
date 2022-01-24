from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="🔍 Начать поиск"),
        KeyboardButton(text="📄 Создать документ"),
    ],
    [
        KeyboardButton(text="⚙ Дополнительные возможности")
    ]
], resize_keyboard=True)
