from utils.db_api import Database


def search_result_string(db: Database, query: str):
    results = db.sort_find(query)
    msgs = []
    msg = f"⚡️ Поиск <b>\"{query}\"</b> по всей Базе Данных"
    if len(results) == 0:
        msg += "\n\nНичего не найдено 😔"
    for sort in results:
        if len(msg) >= 4000:
            msgs.append(msg)
            msg = ""
        sort_id = sort[0]
        sort_name = sort[1]
        sort_count_in_kids = db.sort_count_kids(sort_id)
        sort_count_in_starters = db.sort_count_starters(sort_id)
        sort_count_in_orders = db.sort_count_orders(sort_id)
        sort_count_total = sort_count_in_kids + sort_count_in_starters + sort_count_in_orders
        if sort_count_total == 0:
            msg += f"\n\nСорта 🌸 <b>{sort_name}</b> 🌸 нет в наличии и в заказах 😢"
        else:
            msg += f"\n\n🌸 <b>{sort_name}</b> 🌸"
        if sort_count_in_kids != 0:
            sort_in_kids = db.select_sort_in_kids(sort_id)
            msg += "\n   🌱 " + "\n   🌱 ".join(f"{i[0]} (<b>{i[1]}</b> шт.)" for i in sort_in_kids)
        if sort_count_in_starters != 0:
            sort_in_starters = db.select_sort_in_starters(sort_id)
            msg += "\n   🍀 " + "\n   🍀 ".join(f"{i[0]} (<b>{i[1]}</b> шт.)" for i in sort_in_starters)
        if sort_count_in_orders != 0:
            sort_in_orders = db.select_sort_in_orders(sort_id)
            msg += "\n   📋 " + "\n   📋 ".join(f"{i[0]} (<b>{i[1]}</b> шт.)" for i in sort_in_orders)
        if sort_count_total != 0:
            msg += f"\nВсего: 🌱 {sort_count_in_kids} шт., 🍀 {sort_count_in_starters} шт., 📋 {sort_count_in_orders} шт."
            msg += f"\nВсего в наличии учитывая заказы: {sort_count_in_kids + sort_count_in_starters - sort_count_in_orders}"
    msgs.append(msg)
    return msgs
