from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db

choose_document_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Список лотка/ящика/заказа", callback_data="list_to_docx"),
    ],
    [
        InlineKeyboardButton(text="Списки наличия по n+ шт. и по 1 шт", callback_data="availability_lists"),
    ],
    [
        InlineKeyboardButton(text="Заказы в ящике", callback_data="availability_tables_mode:orders_in_boxes"),
        InlineKeyboardButton(text="Ящики в заказах", callback_data="availability_tables_mode:boxes_in_orders"),
    ],
])

choose_table_to_export_list_keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text="Детки", callback_data="table_to_export:kids"),
        InlineKeyboardButton(text="Стартёры", callback_data="table_to_export:starters"),
        InlineKeyboardButton(text="Заказы", callback_data="table_to_export:orders"),
    ]
])


def choose_list_to_export_keyboard(table_name: str):
    keyboard = InlineKeyboardMarkup(row_width=3)
    lists = None
    if table_name == "kids":
        lists = db.list_titles_kids()
    elif table_name == "starters":
        lists = db.list_titles_starters()
    elif table_name == "orders":
        lists = db.list_titles_orders()
    for list_item in lists:
        list_title = list_item[0]
        list_button = InlineKeyboardButton(text=list_title, callback_data=f"list_to_export:{table_name}:{list_title}")
        keyboard.insert(list_button)
    return keyboard


def choose_list_to_availability_table_keyboard(mode: str):
    keyboard = InlineKeyboardMarkup(row_width=3)
    lists = None
    if mode == "orders_in_boxes":
        lists = db.list_titles_kids()
    elif mode == "boxes_in_orders":
        lists = db.list_titles_orders()
    for list_item in lists:
        list_title = list_item[0]
        list_button = InlineKeyboardButton(text=list_title, callback_data=f"availability_tables_list:{mode}:{list_title}")
        keyboard.insert(list_button)
    all_lists_button = InlineKeyboardButton(text="Все списки", callback_data=f"availability_tables_list:{mode}:all_lists")
    keyboard.add(all_lists_button)
    return keyboard
