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


def set_delivery_for_order(order_id, delivery_id):
    cur.execute('''INSERT INTO Ressending(orderId,deliveryId) VALUES(''' + str(order_id) + "," + str(delivery_id) + ")")


def increase_amount(food_id, amount):
    cur.execute('''SELECT amount from Resfood WHERE Id=''' + str(food_id) + ")")
    rows = cur.fetchall()
    amount += rows[0][0]
    cur.execute('''UPDATE Resfood SET amount=''' + str(amount) + ''' WHERE Id=''' + str(food_id) + ")")


def add_new_restaurant(name, phone_number, area, type, min_order):
    cur.execute(
        '''INSERT INTO RESrestaurant(id,name,phoneNumber,area,type,minOrder,score) VALUES(''' + Id_handler.get_new_id() +
        "," + name + "," + str(phone_number) + " " + area + "," + type + "," + str(min_order) + ",0)")

#new queries
def get_restaurant_orders(restaurant_id):
    cur.execute("select * from Resorder where restaurant_id = " + id_to_str(restaurant_id) + ";")
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
        rows = cur.fetchall()
        arriving_time = rows[0][0]

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

con.commit()
con.close()
