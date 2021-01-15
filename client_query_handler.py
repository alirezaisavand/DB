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

def get_client_info(id):
    cur.execute("select * from cuscustomer where id = '" + id + "';")
    rows = cur.fetchall()
    con.commit()
    for row in rows:
        return row
    return None

def searchـrestaurant (by, str):
    cur.execute("select * from cusrestaurant where " + by + " = '" + str + "';")
    rows = cur.fetchall()
    con.commit()
    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("phone number = ", row[2])
        print("area = ", row[3])
        print("type = ", row[4])
        print("min_order = ", row[5])
        print("score = ", row[6], '\n')

def restaurants_by_score ():
    cur.execute("select * from cusrestaurant;")
    rows = cur.fetchall()

    rows.sort(key=lambda x: x[6])
    rows.reverse()
    con.commit()
    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("phone number = ", row[2])
        print("area = ", row[3])
        print("type = ", row[4])
        print("min_order = ", row[5])
        print("score = ", row[6], '\n')


def search_food (by, str):
    cur.execute("select * from cusfood where " + by + " = '" + str + "';")
    rows = cur.fetchall()
    con.commit()
    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("type = ", row[2])
        print("amount = ", row[3])
        print("description = ", row[4])
        print("price = ", row[5])
        print("restaurant_id = ", row[6])
        print("score = ", row[7], '\n')

def foods_by_score ():
    cur.execute("select * from food;")
    rows = cur.fetchall()

    rows.sort(key=lambda x: x[7])
    rows.reverse()
    con.commit()
    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("type = ", row[2])
        print("amount = ", row[3])
        print("description = ", row[4])
        print("price = ", row[5])
        print("restaurant_id = ", row[6])
        print("score = ", row[7], '\n')


def order_food (customer_id, restaurant_id, food_id):
    cur.execute("select * from customer where id = '" + customer_id + "';")
    rows = cur.fetchall()
    balance = rows[0][4]

    cur.execute("select * from food where id = '" + food_id +
                "' and restaurant_id = '" + restaurant_id + "';")

    rows = cur.fetchall()

    price = rows[0][5]
    amount = rows[0][3]

    if balance < price:
        print("Customer doesn't have enough money!")
    elif amount == 0:
        print("This food is not available!")
    else:
        amount -= 1
        cur.execute("update food set amount = " + str(amount) + " where id = '"
                + food_id + "' and restaurant_id = '" + restaurant_id + "';")

        balance -= price
        cur.execute("update customer set balance = " + str(balance)
                + " where id = '" + customer_id + "';")

        cur.execute("select * from basket where customer_id = '" + customer_id
                    + "' and food_id = '" + food_id + "';")

        rows = cur.fetchall()

        if (len(rows) == 0):
            cur.execute("insert into basket values('" + customer_id + "', '"
                        + food_id + "', 1);")
        else:
            current_amount = rows[0][2]
            new_amount = current_amount + 1
            cur.execute("update basket set amount = " + str(new_amount)
                        + " where customer_id = '" + customer_id
                        + "' and food_id = '" + food_id + "';")

        print("food ordered!")
    con.commit()

def add_customer (username, password, name, area, phoner_number):
    print("NEW CUSTOMER")
    cur.execute("select * from customer where id = '" + username + "';")
    rows = cur.fetchall()
    id=Id_handler.get_new_id()
    if len(rows) == 0:
        cur.execute("insert into customer values('" + id + "', '" + name + "', '"
                    + area + "', '" + phoner_number + "', " + str(0)
                    + ");")
        cur.execute("insert into user_pass values('" + id + "', '" + password + "' , '"+username+"');")
        con.commit()
        return 1
    else:
        print("This user currently exists!")
        con.commit()
        return 0

def check_user_pass(username, password):
    cur.execute("select customer_id from user_pass where username='" +username + "' and  password = '" + password + "';")
    rows = cur.fetchall()
    con.commit()
    if len(rows)==0:
        return -1
    return rows[0][0]

def charge_account(customer_id, amount):
    cur.execute("select * from Cuscustomer where id = " + id_to_str(customer_id) + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("Error")
        return
    balance = rows[0][4] + amount
    cur.execute("update Cuscustomer set balance = " + str(balance) +
                " where id = " + id_to_str(customer_id) + ";")
    con.commit()
    print("account charged successfully")


def rate_food(order_id, food_id, score):
    cur.execute("update CusfoodOrdered set score = " + str(score) +
                " where order_id = " + id_to_str(order_id) + " and food_id = " + id_to_str(food_id) + ';')
    con.commit()

def get_customer_orders(customer_id):
    cur.execute("select restaurant_id, preparing_time, order_time, discount_id, total_price, order_id from Cusorder where customer_id = "
                + id_to_str(customer_id) + " order by order_time;")
    orders_rows = cur.fetchall()
    for row in orders_rows:
        restaurant_id = row[0]
        cur.execute("select name from Cusrestaurant where id = " + id_to_str(restaurant_id) + ";")
        rows = cur.fetchall()
        if len(rows) == 0:
            print("Error")
            return
        restaurant_name = rows[0][0]
        preparing_time = row[1]
        order_time = row[2]
        discount_id = row[3]
        total_price = row[4]
        order_id = row[5]
        cur.execute("select arriving_time from Cussending where order_id = " + id_to_str(order_id) + ";")
        rows = cur.fetchall()
        arriving_time = rows[0][0]


        print("restaurant: " + restaurant_name + " preparing time: " + preparing_time +
              " order time: " + order_time + " arriving time: " + arriving_time + " discount id: " + discount_id +
              " total price: " + total_price)
        cur.execute("select food_id from CusfoodOrdered where order_id = " + id_to_str(order_id) + ";")
        rows = cur.fetchall()
        for row in rows:
            food_id = row[0]
            cur.execute("select name from Cusfood where id = " + id_to_str(food_id) + ";")
            food_rows = cur.fetchall()
            food_name = food_rows[0][0]
            print("food name: " + food_name)
    con.commit()

def receive_order(order_id):
    cur.execute("select * from Cussending where order_id = " + id_to_str(order_id) + ";")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("Error")
        return
    delivery_id = rows[0][1]
    cur.execute("update Cusdelivery set busy = false where id = " + id_to_str(delivery_id) + ";")
    cur.execute("update Cussending set arriving_time = CURRENT_TIMESTAMP where order_id = " + id_to_str(order_id) + ";")
    con.commit()

con.commit()
