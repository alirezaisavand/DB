import psycopg2
import json
import Id_handler

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],
                        password=data["postgresql"]["password"], host=data["postgresql"]["host"],
                        port=data["postgresql"]["port"])
cur = con.cursor()

def get_my_order(deliveryId):
    cur.execute('''SELECT orderId,cost FROM Delsending 
                        WHERE deliveryid='''+str(deliveryId)+''' AND arrivingTime is NULL''')
    rows = cur.fetchall()

    for row in rows:
        return row
    return None

def my_order_arrived(deliveryId):
    cur.execute('''Update Delsending 
                SET arrivingTime = CURRENT_TIMESTAMP
            WHERE deliveryid=''' + str(deliveryId) + ''' AND arrivingTime is NULL''')

def update_delivery_salary(deliveryId,newsalary):
    cur.execute('''Update Deldelivery
                    SET salary ='''+str(newsalary)+'''
                WHERE deliveryid=''' + str(deliveryId))

def add_new_delivery(name,salary,area):
    cur.execute('''INSERT INTO Deldelivery(name,salary,area,busy) VALUES('''+Id_handler.get_new_id()+","+name+","+str(salary)+" "+area+",0")




con.commit()
con.close()


