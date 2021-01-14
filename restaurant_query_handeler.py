import psycopg2
import json
import Id_handler

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],
                       password=data["postgresql"]["password"], host=data["postgresql"]["host"],
                       port=data["postgresql"]["port"])
cur = con.cursor()


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


con.commit()
con.close()
