from aiogram.utils.callback_data import CallbackData

choose_table_to_export_list = CallbackData("table_to_export", "table_name")
choose_list_to_export = CallbackData("list_to_export", "table_name", "list_title")

choose_mode_availability_tables = CallbackData("availability_tables_mode", "mode")
choose_list_availability_tables = CallbackData("availability_tables_list", "mode", "list_title")
