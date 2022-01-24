import os.path

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

KIDS_FILE = os.path.join(DATA_DIR, "kids.xlsx")
STARTERS_FILE = os.path.join(DATA_DIR, "starters.xlsx")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.xlsx")
