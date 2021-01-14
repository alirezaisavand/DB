import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],
                       password=data["postgresql"]["password"], host=data["postgresql"]["host"],
                       port=data["postgresql"]["port"])
cur = con.cursor()

def searchRestaurant (by, str):
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

def restaurantsByScore ():
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


def searchFood (by, str):
    cur.execute("select * from food where " + by + " = '" + str + "';")
    rows = cur.fetchall()

    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("type = ", row[2])
        print("amount = ", row[3])
        print("description = ", row[4])
        print("price = ", row[5])
        print("restaurantid = ", row[6])
        print("score = ", row[7], '\n')

def foodsByScore ():
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
        print("restaurantid = ", row[6])
        print("score = ", row[7], '\n')


def orderFood (customer, restaurant, food):
    cur.execute("select * from customer where name = '" + customer + "';")
    rows = cur.fetchall()
    customerId = rows[0][0]
    balance = rows[0][4]

    cur.execute("select * from restaurant where name = '" + restaurant + "';")
    rows = cur.fetchall()

    restaurantId = rows[0][0]

    cur.execute("select * from food where name = '" + food +
                "' and restaurantId = '" + restaurantId + "';")

    rows = cur.fetchall()

    price = rows[0][5]
    amount = rows[0][3]
    foodId = rows[0][0]

    if balance < price:
        print("Customer doesn't have enough money!")
    elif amount == 0:
        print("This food is not available!")
    else:
        amount -= 1
        cur.execute("update food set amount = " + str(amount) + " where name = '"
                + food + "' and restaurantId = '" + restaurantId + "';")

        balance -= price
        cur.execute("update customer set balance = " + str(balance)
                + " where id = '" + customerId + "';")

        cur.execute("insert into basket values('" + customerId + "', '" + foodId
                + "', 1);")

        print("food ordered!")

def rate_food(food_id, score):


con.commit()
con.close()
