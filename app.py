from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.initialize_db import on_startup_db_initialize
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Инициализируем БД
    on_startup_db_initialize(db)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

