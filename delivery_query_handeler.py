import psycopg2
import json
import Id_handler

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],
                       password=data["postgresql"]["password"], host=data["postgresql"]["host"],
                       port=data["postgresql"]["port"])
cur = con.cursor()


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
    cur.execute("select * from Ressending where deliveryId=" + delivery_id + ";")
    rows = cur.fetchall()

    for row in rows:
        print("order_id = ", row[0])
    con.commit()


#name = input()
#salary = input()
#area = input()

#add_new_delivery(name, salary, area)

#cur.execute("select * from delivery;")
#rows = cur.fetchall()

#for row in rows:
#    print("id = ", row[0])
#    print("name = ", row[1])
#    print("salary = ", row[2])
#    print("area = ", row[3])
#    print("busy = ", row[4])

#print("done!")
#def set_delivery_for_order(order_id, delivery_id):
#    cur.execute(
#        '''INSERT INTO Ressending(orderId,deliveryId) VALUES(''' + str(order_id) + "," + str(delivery_id) + ")")

con.commit()
