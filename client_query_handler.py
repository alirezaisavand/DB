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
    for row in rows:
        return row
    return None


def get_condition(by, ans):
    if len(by) == 0:
        return ""
    st = " where "
    for i in range(0, len(by)):
        if i != 0:
            st += " and "
        if by[i] == "score":
            st += by[i] + " >= '" + ans[i] + "'"
        elif by[i] == "price":
            if ans[i] > 0:
                st += by[i] + " >= '" + ans[i] + "'"
            else:
                st += by[i] + " <= '" + ans[i] + "'"
        else:
            st += by[i] + " = '" + ans[i] + "'"
    return st


def searchـrestaurant(by, str):
    st = get_condition(by, str)
    cur.execute("select * from cusrestaurant " + st + ";")
    rows = cur.fetchall()
    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("phone number = ", row[2])
        print("area = ", row[3])
        print("type = ", row[4])
        print("min_order = ", row[5])
        print("score = ", row[6], '\n')
    return rows


def restaurants_by_score():
    cur.execute("select * from cusrestaurant;")
    rows = cur.fetchall()

    rows.sort(key=lambda x: x[6])
    rows.reverse()
    for row in rows:
        print("id = ", row[0])
        print("name = ", row[1])
        print("phone number = ", row[2])
        print("area = ", row[3])
        print("type = ", row[4])
        print("min_order = ", row[5])
        print("score = ", row[6], '\n')
    return rows


def get_all_restaurant_specific_colum(str):
    cur.execute("select distinct " + str + " from cusrestaurant;")
    rows = cur.fetchall()
    return rows


def get_all_food_specific_colum(str):
    cur.execute("select distinct " + str + " from cusfood;")
    rows = cur.fetchall()
    return rows


def search_food(by, str):
    cur.execute("select * from cusfood" + get_condition(by, str) + ";")
    rows = cur.fetchall()
    return rows


def foods_by_score():
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
    return rows


def order_food(customer_id, restaurant_id, food_id):
    cur.execute("select * from food where id = '" + food_id +
                "' and restaurant_id = '" + restaurant_id + "';")
    rows = cur.fetchall()

    amount = rows[0][3]
    if amount == 0:
        print("This food is not available!")
    else:
        amount -= 1
        cur.execute("update food set amount = " + str(amount) + " where id = '"
                    + food_id + "' and restaurant_id = '" + restaurant_id + "';")

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


# cur.execute('''CREATE VIEW CusdiscountCode AS SELECT id,percentage,max,customer_id FROM discountCode ''')
def add_discount_code(client_id, percentage, max):
    id = Id_handler.get_new_id()
    cur.execute("insert into cusdiscountCode values('" + id + "', " + str(percentage) + ", "
                + str(max) + ", '" + client_id + "' , false ); ")
    con.commit()
    return id


def add_customer(username, password, name, area, phoner_number):
    print("NEW CUSTOMER")
    cur.execute("select * from user_pass where customer_id = '" + username + "';")
    rows = cur.fetchall()
    id = username
    if len(rows) == 0:
        cur.execute("insert into customer values('" + id + "', '" + name + "', '"
                    + area + "', '" + phoner_number + "', " + str(0)
                    + ");")
        cur.execute("insert into user_pass values('" + id + "', '" + password + "');")
        con.commit()
        return id
    else:
        print("This user currently exists!")
        con.commit()
        return 0


def check_user_pass(username, password):
    cur.execute(
        "select customer_id from user_pass where customer_id='" + username + "' and  password = '" + password + "';")
    rows = cur.fetchall()
    con.commit()
    if len(rows) == 0:
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


def get_customer_basket(customer_id):
    cur.execute(
        "select cusfood.name, basket.amount, cusfood.id from basket inner join cusfood ON(basket.food_id=cusfood.id) where customer_id = '"
        + customer_id + "';")
    return cur.fetchall()


def add_delivery_score(order_id, score):
    cur.execute("update cussending set score=" + str(
        score) + " where order_id='" + order_id + "';")
    con.commit()


def get_order_data(order_id):
    cur.execute("select * from cusorder where id = '"
                + order_id + "';")
    return cur.fetchall()


def get_sending_data(order_id):
    cur.execute("select * from cussending where order_id = '"
                + order_id + "';")
    rows = cur.fetchall()
    if len(rows) == 0:
        return [["?"] * 10]
    else:
        return rows


def get_customer_orders(customer_id):
    cur.execute(
        "select cusorder.id,cusrestaurant.name,cusorder.order_time,cusorder.total_price from Cusorder INNER join cusrestaurant on (cusorder.restaurant_id=cusrestaurant.id) where customer_id = "
        + id_to_str(customer_id) + " order by order_time;")
    orders_rows = cur.fetchall()
    return orders_rows


#  ans=[]
#  for row in orders_rows:
#     restaurant_id = row[0]
#     cur.execute("select name from Cusrestaurant where id = " + id_to_str(restaurant_id) + ";")
#     rows = cur.fetchall()
#     if len(rows) == 0:
#         print("Error")
#         return
#     restaurant_name = rows[0][0]
#     preparing_time = row[1]
#     discount_id = row[3]
#     total_price = row[4]
#     order_time = row[5]
#     cur.execute("select arriving_time from Cussending where order_id = " + id_to_str(order_id) + ";")
#     rows = cur.fetchall()
#     arriving_time = rows[0][0]

#    print("restaurant: " + restaurant_name + " preparing time: " + preparing_time +
#          " order time: " + order_time + " arriving time: " + arriving_time + " discount id: " + discount_id +
#          " total price: " + total_price)
#    ans.append([order_id,restaurant_name,order_time,total_price])
# return ans

def find_food_id(order_id, food_name):
    cur.execute("select food_id from cusfoodordered INNER JOIN CUSfood ON(cusfoodordered.food_id=cusfood.id) "
                "where cusfoodordered.order_id='" + order_id + "' and cusfood.name='" + food_name + "';")
    return cur.fetchall()[0][0]


# cur.execute('''CREATE VIEW CusfoodOrdered AS SELECT order_id,food_id,score,amount FROM food_ordered''')

def add_score(order_id, food_id, score):
    cur.execute("update cusfoodordered set score=" + str(
        score) + " where order_id='" + order_id + "' and food_id='" + food_id + "';")
    con.commit()


# cur.execute('''CREATE VIEW CusdiscountCode AS SELECT id,percentage,max,customer_id FROM discountCode ''')
def get_customer_discounts(client_id):
    cur.execute("select id,percentage,max FROM cusdiscountCode "
                "where customer_id='" + client_id + "' and used=false;")
    return cur.fetchall()


def get_basket_price(client_id):
    cur.execute("select SUM(cusfood.price*basket.amount) FROM cusfood inner join basket ON(cusfood.id=basket.food_id)"
                "where basket.customer_id='" + client_id + "';")
    return cur.fetchall()[0][0]


def buy_basket_foods(client_id, discount_id=None):  # return order_id
    rows = get_customer_basket(client_id)
    if len(rows) == 0:
        print("BUY SOMETHING FIRST")
        return "-1"
    first_food_id = rows[0][2]

    cur.execute("select restaurant_id from cusfood where id='" + first_food_id + "';")
    restaurant_id = cur.fetchall()[0][0]

    cur.execute("select SUM(cusfood.price*basket.amount) FROM cusfood inner join basket ON(cusfood.id=basket.food_id)"
                "where basket.customer_id='" + client_id + "';")
    total_price = cur.fetchall()[0][0]

    cur.execute("select * from customer where id = '" + client_id + "';")
    rows = cur.fetchall()
    balance = rows[0][4]
    if balance < total_price:
        print("Customer doesn't have enough money!")
        return
    balance -= total_price
    cur.execute("update customer set balance = " + str(balance)
                + " where id = '" + client_id + "';")

    order_id = Id_handler.get_new_id()
    if discount_id is None:
        cur.execute("insert into cusorder (id,restaurant_id,customer_id,order_time,total_price)"
                    " values('" + order_id + "','" + restaurant_id + "','" + client_id + "',current_timestamp,"
                    + str(total_price) + ");")
    else:
        cur.execute("insert into cusorder (id,restaurant_id,customer_id,order_time,discount_id,total_price)"
                    " values('" + order_id + "','" + restaurant_id + "','" + client_id + "',current_timestamp,'"
                    + discount_id + "'," + str(total_price) + ");")
        cur.execute("update cusdiscountcode set used = true where id='" + discount_id + "';")
        # bargardonim
    cur.execute("insert into CusfoodOrdered (order_id,food_id,amount) select "
                "'" + order_id + "',food_id,amount from basket where customer_id='" + client_id + "';")

    cur.execute("DELETE from basket where customer_id='" + client_id + "';")
    con.commit()
    return order_id


def get_foods_of_order(order_id):
    cur.execute("select Cusfood.name,Cusfood.type,Cusfood.Price,CusfoodOrdered.amount,CusfoodOrdered.score "
                "from CusfoodOrdered INNER JOIN Cusfood ON(cusfoodOrdered.food_Id=cusfood.id) where order_id = '" +
                order_id + "';")
    rows = cur.fetchall()
    return rows

    # for row in rows:
    #    food_id = row[0]
    #    cur.execute("select name from Cusfood where id = " + id_to_str(food_id) + ";")
    #    food_rows = cur.fetchall()
    #    food_name = food_rows[0][0]
    #    print("food name: " + food_name)
    # con.commit()


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
