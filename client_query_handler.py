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

def check_user_pass(id,password):
    cur.execute("select * from user_pass where customer_id='" + id + "', password = '" + password + "';")
    rows = cur.fetchall()

    for row in rows:
        return 1
    return 0

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
        print("restaurant_id = ", row[6])
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

def add_customer (id, password, name, area, phoner_number, balance):
    cur.execute("select * from customer where id = '" + id + "';")
    rows = cur.fetchall()

    if (len(rows) == 0):
        cur.execute("insert into customer values('" + id + "', '" + name + "', '"
                    + area + "', '" + phoner_number + "', " + str(balance)
                    + ");")
        cur.execute("insert into user_pass values('" + id + "', '" + password
                    + "');")
    else:
        print("This user currently exists!")

add_customer(id, password, name, area, phone_number, balance)

def rate_food(food_id, order_id, score):
    cur.execute("update CusfoodOrdered set score = " + str(score) + " where food_id = " + food_id + " and order_id = " + order_id + ";")

def charge_account(customer_id, amount):
    cur.execute("update Cuscustomer set balance = " + str(amount) + " where id = " + customer_id + ";")


def rate_food(food_id, score):
    cur.execute("select * from foodRatings")

con.commit()
con.close()
