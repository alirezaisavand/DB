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
    cur.execute('''SELECT orderId,cost FROM Delsending 
                        WHERE deliveryid=''' + str(delivery_id) + ''' AND arrivingTime is NULL''')
    rows = cur.fetchall()

    for row in rows:
        return row
    return None


def my_order_arrived(delivery_id):
    cur.execute('''Update Delsending 
                SET arrivingTime = CURRENT_TIMESTAMP
            WHERE deliveryid=''' + str(delivery_id) + ''' AND arrivingTime is NULL''')
    con.commit()


def update_delivery_salary(delivery_id, new_salary):
    cur.execute('''Update Deldelivery
                    SET salary =''' + str(new_salary) + '''
                WHERE deliveryid=''' + str(delivery_id))
    con.commit()


def add_new_delivery(name, salary, area):
    cur.execute("INSERT INTO Deldelivery VALUES('" + Id_handler.get_new_id() + "','" + name + "'," + str(
            salary) + ",'" + area + "',false);")
    print("INSERT INTO Deldelivery VALUES('" + Id_handler.get_new_id() + "','" + name + "'," + str(
            salary) + ",'" + area + "',false);")
    con.commit()

def get_delivery_basket(delivery_id):
    cur.execute("select * from Delsending where delivery_id='" + delivery_id + "';")
    rows = cur.fetchall()

    for row in rows:
        print("order_id = ", row[0])
    con.commit()

    return rows

def check_name(name):
    cur.execute(
        "select id from delivery where name=" + id_to_str(
            name) + ";")
    rows = cur.fetchall()
    con.commit()
    if len(rows) == 0:
        return -1
    return rows[0][0]

con.commit()
