import psycopg2
import json
import Id_handler

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
    cur.execute('''UPDATE Resorder SET preparingTime = CURRENT_TIMESTAMP WHERE ordertId=''' + str(order_id))


def get_not_completed_order(restaurant_id):
    cur.execute('''SELECT id from Resorder WHERE restaurantId=''' + str(restaurant_id) + '''
    AND preparingTime IS NULL'''
                )
    return cur.fetchall()


def add_food_to_restaurant(restaurant_id, food_name, food_type, food_description, food_price):
    id = Id_handler.get_new_id()
    cur.execute("INSERT INTO RESfood VALUES('" + id + "','" + food_name + "','" + food_type + "',1,'"
                + food_description + "'," + str(food_price) + ",'" + restaurant_id + "');")
    con.commit()
    return id


def set_delivery_for_order(order_id, delivery_id):
    cur.execute('''INSERT INTO Ressending(orderId,deliveryId) VALUES(''' + str(order_id) + "," + str(delivery_id) + ")")


def increase_amount(food_id, amount):
    cur.execute('''SELECT amount from Resfood WHERE Id=''' + str(food_id) + ")")
    rows = cur.fetchall()
    amount += rows[0][0]
    cur.execute('''UPDATE Resfood SET amount=''' + str(amount) + ''' WHERE Id=''' + str(food_id) + ")")
    con.commit()


# new queries
def get_restaurant_orders(restaurant_id, filter_arrived):
    cur.execute("select * from Resorder where restaurant_id = " + id_to_str(restaurant_id) + " order by order_time;")
    orders_rows = cur.fetchall()
    for row in orders_rows:
        customer_id = row[3]
        cur.execute("select name from Rescustomer where id = " + id_to_str(customer_id) + ";")
        rows = cur.fetchall()
        if len(rows) == 0:
            print("Error")
            return
        customer_name = rows[0][0]
        preparing_time = row[2]
        order_time = row[4]
        total_price = row[5]
        order_id = row[0]
        cur.execute("select arriving_time from Ressending where order_id = " + id_to_str(order_id) + ";")
        arriving_time = cur.fetchall()[0][0]

        if filter_arrived:
            cur.execute("select order_id from Ressending where order_id = " + id_to_str(
                order_id) + " and arriving_time is null;")
            if len(cur.fetchall()) == 0:
                continue

        print("customer name: " + customer_name + " preparing time: " + preparing_time +
              " order time: " + order_time + " arriving time: " + arriving_time +
              " total price: " + total_price)
        cur.execute("select food_id from ResfoodOrdered where order_id = " + id_to_str(order_id) + ";")
        rows = cur.fetchall()
        for row in rows:
            food_id = row[0]
            cur.execute("select name from Resfood where id = " + id_to_str(food_id) + ";")
            food_rows = cur.fetchall()
            food_name = food_rows[0][0]
            print("food name: " + food_name)

def check_user_pass(username, password):
    cur.execute(
        "select restaurant_id from res_user_pass where username=" + id_to_str(username) + " and  password = " + id_to_str(password) + ";")
    rows = cur.fetchall()
    con.commit()
    if len(rows) == 0:
        return -1
    return rows[0][0]


def add_restaurant(username, password, name, area, phone_number, type, min_order):
    print("NEW RESTAURANT")
    cur.execute("select * from res_user_pass where username = " + id_to_str(username) + ";")
    rows = cur.fetchall()
    id = Id_handler.get_new_id()
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
                    id_to_str(password) + ", " +
                    id_to_str(username) +
                    ");"
                    )
        con.commit()
        return 1
    else:
        print("this user currently exists!")
        con.commit()
        return 0