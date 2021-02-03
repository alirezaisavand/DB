import psycopg2
import json
import Id_handler
import client_query_handler

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],
                       password=data["postgresql"]["password"], host=data["postgresql"]["host"],
                       port=data["postgresql"]["port"])
cur = con.cursor()


def id_to_str(id):
    str_id = "\'" + id + "\'"
    return str_id


def food_is_ready(order_id):
    cur.execute("UPDATE Resorder SET preparing_Time = CURRENT_TIMESTAMP WHERE id=" + id_to_str(order_id) + ";")
    con.commit()


def get_not_completed_order(restaurant_id):
    cur.execute("SELECT id from Resorder WHERE restaurant_id=" + id_to_str(restaurant_id) + " AND preparing_time IS NULL;")
    con.commit()
    return cur.fetchall()


def add_food_to_restaurant(restaurant_id, food_name, food_type, food_description, food_price):
    food_id = Id_handler.get_new_id()
    try:
        cur.execute("INSERT INTO RESfood VALUES('" + food_id + "','" + food_name + "','" + food_type + "',0,'"
                + food_description + "'," + str(food_price) + ",'" + restaurant_id + "');")

        con.commit()
        return True
    except:
        return False

    return False


def set_delivery_for_order(order_id, delivery_id):
    cur.execute('''INSERT INTO Ressending VALUES(''' + id_to_str(order_id) + "," + id_to_str(delivery_id) + ", null);")
    cur.execute("update resdelivery set busy = True where id = " + id_to_str(delivery_id) + ";")
    con.commit()

def get_free_deliveries(restaurant_id):
    info = get_restaurant_info(restaurant_id)
    area = info[3]
    cur.execute("select * from resdelivery where area = " + id_to_str(area) + " and busy = False;")
    return cur.fetchall()

def increase_amount(food_id, amount):
    cur.execute("SELECT amount from Resfood WHERE id=" + id_to_str(food_id))
    rows = cur.fetchall()
    print(len(rows))
    amount += rows[0][0]
    cur.execute("UPDATE Resfood SET amount=" + str(amount) + " WHERE id=" + id_to_str(food_id))
    con.commit()

def is_arrived(order_id):
    if not is_set_delivery(order_id):
        return False
    cur.execute("select order_id from Ressending where order_id = " + id_to_str(
        order_id) + " and arriving_time is null;")
    con.commit()
    if len(cur.fetchall()) == 0:
        return True
    return False
# new queries

def get_customer_name(customer_id):
    cur.execute("select name from Rescustomer where id = " + id_to_str(customer_id) + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("Error")
        return None
    return rows[0][0]

def get_arriving_time(order_id):
    cur.execute("select arriving_time from Ressending where order_id = " + id_to_str(order_id) + ";")
    row = cur.fetchall()
    if len(row):
        return row[0][0]
    return "Not Send"

def is_set_delivery(order_id):
    cur.execute("select order_id from Ressending where order_id = " + id_to_str(order_id) + ";")
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    return False

def get_order_foods(order_id):
    cur.execute("select food_id from ResfoodOrdered where order_id = " + id_to_str(order_id) + ";")
    rows = cur.fetchall()
    food_ids = []
    for i in rows:
        food_ids.append(i[0])
    print(food_ids)
    return food_ids

def get_food_name(food_id):
    cur.execute("select name from Resfood where id = " + id_to_str(food_id) + ";")
    return cur.fetchall()[0][0]

def get_food_names(foods):
    food_names = []
    print(foods)
    for food_id in foods:
        food_name = get_food_name(food_id)
        food_names.append(food_name)
    return food_names

def get_order_food_names(order_id):
    foods = get_order_foods(order_id)
    food_names = get_food_names(foods)
    return food_names

def is_ready(order_id):
    cur.execute("select id from Resorder where id = " + id_to_str(order_id) + " and preparing_time is not null;")
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    return False

def get_restaurant_orders(restaurant_id, filter_arrived, filter_set_delivery, filter_ready):
    cur.execute("select * from Resorder where restaurant_id = " + id_to_str(restaurant_id) + " order by order_time;")
    orders_rows = cur.fetchall()
    results = []
    for row in orders_rows:
        customer_id = row[3]

        customer_name = get_customer_name(customer_id)
        preparing_time = row[2]
        order_time = row[4]
        total_price = row[5]
        order_id = row[0]
        if filter_arrived and is_arrived(order_id):
            continue

        if filter_set_delivery and is_set_delivery(order_id):
            continue

        if filter_ready and is_ready(order_id):
            continue

        arriving_time = get_arriving_time(order_id)




        results.append([order_id, customer_name, preparing_time, order_time, total_price, arriving_time])

    return results

def check_user_pass(id, password):
    cur.execute(
        "select restaurant_id from res_user_pass where restaurant_id=" + id_to_str(id) + " and  password = " + id_to_str(password) + ";")
    rows = cur.fetchall()
    con.commit()
    if len(rows) == 0:
        return -1
    return rows[0][0]


def add_restaurant(id, password, name, area, phone_number, type, min_order):
    print("NEW RESTAURANT")
    cur.execute("select * from res_user_pass where restaurant_id = " + id_to_str(id) + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        cur.execute("insert into restaurant values(" +
                    id_to_str(id) + ", " +
                    id_to_str(name) + ", " +
                    id_to_str(phone_number) + ", " +
                    id_to_str(area) + ", " +
                    id_to_str(type) + ", " +
                    "0, " +
                    str(min_order) +
                    ");"
                    )
        cur.execute("insert into res_user_pass values(" +
                    id_to_str(id) + ", " +
                    id_to_str(password) +
                    ");"
                    )
        con.commit()
        return True
    else:
        print("this user currently exists!")
        con.commit()
        return False

def get_restaurant_info(id):
    cur.execute("select * from Resrestaurant where id = " + id_to_str(id) + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        return None
    return rows[0]

def get_restaurant_foods(restaurant_id):
    cur.execute("select id, name from food where restaurant_id = " + id_to_str(restaurant_id) + ";")
    rows = cur.fetchall()
    return rows