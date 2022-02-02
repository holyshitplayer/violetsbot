from utils.db_api import Database


def availability_lists_document(db: Database, n: int):
    with open("data/files/availability_n.txt", "w", encoding="utf-8") as a_n, open("data/files/availability_1.txt", "w", encoding="utf-8") as a_1:
        sorts = db.select_filtered_sorts()
        for sort in sorts:
            sort_id = sort[0]
            sort_name = sort[1]
            sort_count_in_kids = db.sort_count_kids(sort_id)
            sort_count_in_starters = db.sort_count_starters(sort_id)
            sort_count_in_orders = db.sort_count_orders(sort_id)
            sort_count_total = sort_count_in_kids + sort_count_in_starters - sort_count_in_orders
            if sort_count_in_kids >= 1 and sort_count_total >= n:
                a_n.write(f'{sort_name} (🌱 {sort_count_in_kids}, 🍀 {sort_count_in_starters}, 📋 {sort_count_in_orders}),\n')
            elif sort_count_total == 1:
                a_1.write(f'{sort_name} (🌱 {sort_count_in_kids}, 🍀 {sort_count_in_starters}, 📋 {sort_count_in_orders})\n')
