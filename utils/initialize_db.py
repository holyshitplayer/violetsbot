import logging

from utils.db_api import Database
from utils.misc.export_excel_data import sorts_values_from_excel, content_values_from_excel
from utils.misc.load_xlsx_sheet import load_kids_sheet, load_starters_sheet, load_orders_sheet


def on_startup_db_initialize(db: Database):
    logging.info("Trying to initialize DB...")

    try:
        db.drop_table_sorts()
        db.drop_table_kids()
        db.drop_table_starters()
        db.drop_table_orders()

        db.create_table_sorts()
        db.create_table_kids()
        db.create_table_starters()
        db.create_table_orders()

        db.fill_table_sorts(sorts_values_from_excel())
        db.fill_table_kids(content_values_from_excel(db, load_kids_sheet()))
        db.fill_table_starters(content_values_from_excel(db, load_starters_sheet()))
        db.fill_table_orders(content_values_from_excel(db, load_orders_sheet()))

    except Exception as err:
        logging.exception(err)

    logging.info("DB was successfully initialized")
