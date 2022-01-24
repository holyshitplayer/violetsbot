import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from keyboards.default import main_keyboard
from keyboards.inline import choose_document_keyboard, choose_table_to_export_list_keyboard, \
    choose_list_to_export_keyboard, choose_list_to_availability_table_keyboard
from keyboards.inline.callback_datas import choose_table_to_export_list, choose_list_to_export, \
    choose_mode_availability_tables, choose_list_availability_tables
from loader import dp, db, bot
from utils.misc.create_availability_lists import create_availability_lists
from utils.misc.create_availability_tables import availability_tables_document, availability_table_document
from utils.misc.export_list_to_docx import export_list_to_docx


@dp.message_handler(text="📄 Создать документ")
async def create_document(message: types.Message):
    await message.answer("Какой документ необходимо создать?", reply_markup=choose_document_keyboard)


@dp.callback_query_handler(text="list_to_docx")
async def list_to_docx(call: CallbackQuery):
    await call.message.edit_text("Выберите из какой таблицы необходимо создать список", reply_markup=choose_table_to_export_list_keyboard)


@dp.callback_query_handler(choose_table_to_export_list.filter())
async def list_to_docx(call: CallbackQuery, callback_data: dict):
    table_name = callback_data.get("table_name")
    await call.message.edit_text("Какой список Вам нужен?", reply_markup=choose_list_to_export_keyboard(table_name))


@dp.callback_query_handler(choose_list_to_export.filter())
async def list_to_docx(call: CallbackQuery, callback_data: dict):
    table_name = callback_data.get("table_name")
    list_title = callback_data.get("list_title")
    docx_path = export_list_to_docx(db, table_name, list_title)
    await call.message.edit_text(f"Ваш файл <b>{os.path.basename(docx_path)}</b> готов!")
    with open(docx_path, "rb") as doc:
        await call.message.answer_document(doc)
        os.remove(docx_path)


@dp.callback_query_handler(text="availability_lists")
async def availability_lists(call: CallbackQuery, state: FSMContext):
    cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Отменить")]], resize_keyboard=True)
    await call.message.edit_text("Списки наличия по n+ шт. и по 1 шт")
    await bot.send_message(call.message.chat.id, "Введите количество <b>n</b>, по которому сформировать список наличия", reply_markup=cancel_keyboard)
    await state.set_state("availability_number")


@dp.message_handler(text="❌ Отменить", state="availability_number")
async def availability_lists(message: types.Message, state: FSMContext):
    await message.answer("Сделать что нибудь ещё? ✨", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(state="availability_number")
async def availability_lists(message: types.Message, state: FSMContext):
    try:
        n = int(message.text)
        if n > 30:
            await message.answer("Введённое значение слишком большое, попробуйте поменьше")
        else:
            await message.answer("Списки наличия создаются, подождите")
            create_availability_lists(db, n)
            with open("data/files/availability_n.txt", "rb") as a_n, open("data/files/availability_1.txt", "rb") as a_1:
                docs = types.MediaGroup()
                docs.attach_document(a_n)
                docs.attach_document(a_1)
                await message.answer(f"Списки наличии по {n}+ шт. и по 1 шт.")
                await message.answer_media_group(docs)
            await message.answer("Сделать что нибудь ещё? ✨", reply_markup=main_keyboard)
            await state.finish()
    except ValueError:
        await message.answer("Введите корректное значение")


@dp.callback_query_handler(choose_mode_availability_tables.filter())
async def availability_tables(call: CallbackQuery, callback_data: dict):
    mode = callback_data.get("mode")
    await call.message.edit_text("Какой список Вам нужен?", reply_markup=choose_list_to_availability_table_keyboard(mode))


@dp.callback_query_handler(choose_list_availability_tables.filter(list_title="all_lists"))
async def availability_tables(call: CallbackQuery, callback_data: dict):
    mode = callback_data.get("mode")
    await call.message.edit_text("Таблицы наличия создаются, подождите")
    docx_path = availability_tables_document(db, mode)
    await call.message.edit_text(f"Ваш файл <b>{os.path.basename(docx_path)}</b> готов!")
    with open(docx_path, "rb") as doc:
        await call.message.answer_document(doc)


@dp.callback_query_handler(choose_list_availability_tables.filter())
async def availability_tables(call: CallbackQuery, callback_data: dict):
    mode = callback_data.get("mode")
    list_title = callback_data.get("list_title")
    await call.message.edit_text("Таблицы наличия создаются, подождите")
    docx_path = availability_table_document(db, mode, list_title)
    await call.message.edit_text(f"Ваш файл <b>{os.path.basename(docx_path)}</b> готов!")
    with open(docx_path, "rb") as doc:
        await call.message.answer_document(doc)
