import sqlite3

conn = sqlite3.connect("login_db.db")

def db_retrieve(all=False):
    menu = [
        "biryani",
        "dosa",
        "drink",
        "french",
        "fried",
        "idli",
        "noodles",
    ]
    main_query=""
    if all:
        main_query = "SELECT * FROM orders"
    else:
        main_query = "SELECT * FROM orders WHERE delivered=0"
    
    return_dict = {}
    retrieved_info = []

    list_var = conn.execute(main_query)
    rows = list(list_var.fetchall())
    for row in rows:
        temp_list = []
        id = row[0]

        for item in menu:
            condition = "company_name" if item=="drink" else item+"_type"
            query = f"SELECT * FROM {item} WHERE order_no={id} AND {condition}!='Null';"
            items = conn.execute(query)
            for item in items:
                if item[2]!=0:
                    temp_list.append(item)
        retrieved_info.append(temp_list)
        temp_list = []
    
    for items in retrieved_info:
        temp_list, id = [], 0

        for item in items:
            if item:
                temp_list.append((item[1], item[2]))
                id = item[0]
        return_dict[id] = temp_list
        temp_list = []
        id = 0
        
    return return_dict

def order_ids(all=False):
    query=""
    if all:
        query = "SELECT order_no FROM orders"
    else:
        query = "SELECT order_no FROM orders WHERE delivered=0"

    return_id = []
    ids = conn.execute(query)
    for id in ids:
        return_id.append(id[0])
    return return_id
