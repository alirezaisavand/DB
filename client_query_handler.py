import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],
                       password=data["postgresql"]["password"], host=data["postgresql"]["host"],
                       port=data["postgresql"]["port"])
cur = con.cursor()

def searchـrestaurant (by, str):
    cur.execute("select * from restaurant where " + by + " = '" + str + "';")
    rows = cur.fetchall()

    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("phone number = ", row[2])
        print("area = ", row[3])
        print("type = ", row[4])
        print("minOrder = ", row[5])
        print("score = ", row[6], '\n')

def restaurants_by_score ():
    cur.execute("select * from restaurant;")
    rows = cur.fetchall()

    rows.sort(key=lambda x: x[6])
    rows.reverse()

    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("phone number = ", row[2])
        print("area = ", row[3])
        print("type = ", row[4])
        print("minOrder = ", row[5])
        print("score = ", row[6], '\n')


def search_food (by, str):
    cur.execute("select * from food where " + by + " = '" + str + "';")
    rows = cur.fetchall()

    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("type = ", row[2])
        print("amount = ", row[3])
        print("description = ", row[4])
        print("price = ", row[5])
        print("resturant_id = ", row[6])
        print("score = ", row[7], '\n')

def foods_by_score ():
    cur.execute("select * from food;")
    rows = cur.fetchall()

    rows.sort(key=lambda x: x[7])
    rows.reverse()

    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("type = ", row[2])
        print("amount = ", row[3])
        print("description = ", row[4])
        print("price = ", row[5])
        print("resturant_id = ", row[6])
        print("score = ", row[7], '\n')


def order_food (customer_id, resturant_id, food_id):
    cur.execute("select * from customer where id = '" + customer_id + "';")
    rows = cur.fetchall()
    balance = rows[0][4]

    cur.execute("select * from food where id = '" + food_id +
                "' and resturant_id = '" + resturant_id + "';")

    rows = cur.fetchall()

    price = rows[0][5]
    amount = rows[0][3]

    if balance < price:
        print("Customer doesn't have enough money!")
    elif amount == 0:
        print("This food is not available!")
    else:
        amount -= 1
        cur.execute("update food set amount = " + str(amount) + " where name = '"
                + food_id + "' and resturant_id = '" + resturant_id + "';")

        balance -= price
        cur.execute("update customer set balance = " + str(balance)
                + " where id = '" + customer_id + "';")

        cur.execute("insert into basket values('" + customer_id + "', '" + food_id
                + "', 1);")

        print("food ordered!")

def add_client (id, name, area, phoner_number, balance):
    cur.execute("insert into customer values('" + id + "', '" + name + "', '"
                + area + "', '" + phoner_number + "', " + str(balance)
                + ");")

def rate_food(food_id, order_id, score):
    cur.execute("update CusfoodOrdered set score = " + str(score) + " where food_id = " + food_id + " and order_id = " + order_id + ";")

def charge_account(customer_id, amount):
    cur.execute("update Cuscustomer set balance = " + str(amount) + " where id = " + customer_id + ";")

con.commit()
con.close()
