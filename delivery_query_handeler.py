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

def get_my_order(delivery_id):
    cur.execute('''SELECT order_id,cost FROM Delsending 
                        WHERE delivery_id=''' + id_to_str(delivery_id) + ''' AND arriving_time is NULL''')
    rows = cur.fetchall()

    return rows


def my_order_arrived(delivery_id):
    cur.execute('''Update Delsending 
                SET arriving_time = CURRENT_TIMESTAMP
            WHERE delivery_id=''' + id_to_str(delivery_id) + ''' AND arriving_time is NULL''')
    con.commit()


def update_delivery_salary(delivery_id, new_salary):
    cur.execute('''Update Deldelivery
                    SET salary =''' + str(new_salary) + '''
                WHERE delivery_id=''' + id_to_str(delivery_id))
    con.commit()


def add_new_delivery(name, salary, area, user, pas):
    id = user
    try:
        cur.execute("insert into delivery values('" + id + "','" + name + "'," + str(
                salary) + ",'" + area + "',false);")
        cur.execute("insert into del_user_pass values('" + id + "', '" + pas + "')")
    except:
        return -1

    con.commit()

def get_delivery_basket(delivery_id):
    cur.execute("select * from Ressending where delivery_id='" + delivery_id + "';")
    rows = cur.fetchall()

#    for row in rows:
#        print("order_id = ", row[0])
    con.commit()

    return rows

def find_all_delivery_orders(not_arrived):
    if not_arrived:
        cur.execute('''select * from Delsending where arriving_time is NULL''')
    else:
        cur.execute('''select * from Delsending''')

    rows = cur.fetchall()
    con.commit()

    return rows

def find_delivery_basket(delivery_id, mine, not_arrived):
    if mine:
        if not_arrived:
            return get_delivery_basket(delivery_id)
        return get_my_order(delivery_id)

    else:
        return find_all_delivery_orders(not_arrived)

def get_order_information(order_id):
    cur.execute('''select * from Resorder where id = ''' + id_to_str(id))
    rows = cur.fetchall()
    con.commit()
    return rows

def find_username(username):
    cur.execute('''select * from del_user_pass where delivery_id = ''' + id_to_str(username))
    rows = cur.fetchall()
    con.commit()
    return rows

def check_user_pass(user, pas):
    cur.execute("select delivery_id from del_user_pass where delivery_id = " + id_to_str(user) +
                "and password = " + id_to_str(pas) + ";")
    rows = cur.fetchall()
    con.commit()
    if len(rows) == 0:
        return -1
    return rows[0][0]

con.commit()
