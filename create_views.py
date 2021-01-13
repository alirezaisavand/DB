import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])

cur = con.cursor()
cur.execute('''CREATE VIEW Cusfood AS
SELECT id,name,type,amount,description,price,restaurantId,score
FROM food
''')
cur.execute('''CREATE VIEW Cusrestaurant AS
SELECT id,name,phoneNumber,area,type,minOrder,score
FROM restaurant
''')
cur.execute('''CREATE VIEW Cusdelivery AS
SELECT id,name
FROM delivery
''')
cur.execute('''CREATE VIEW CusdiscountCode AS
SELECT id,percentage,max,custId
FROM discountCode
''')
cur.execute('''CREATE VIEW Cuscustomer AS
SELECT id,name,area,phoneNumber,balance
FROM customer
''')
cur.execute('''CREATE VIEW Cusbasket AS
SELECT customerid,foodId,amount
FROM basket
''')
cur.execute('''CREATE VIEW Cusorder AS
SELECT id,restaurantId,preparingTime,customerId,orderTime,discountId
FROM orderr
''')
cur.execute('''CREATE VIEW Cussending AS
SELECT orderId,deliveryId,score,arrivingTime,cost
FROM sending
''')
cur.execute('''CREATE VIEW CusfoodOrdered AS
SELECT orderId,foodId,score
FROM foodOrdered
''')


con.commit()
print("views of Customer created successfully")

cur.execute('''CREATE VIEW Delrestaurant AS
SELECT id,name,phoneNumber,area
FROM restaurant
''')
cur.execute('''CREATE VIEW Deldelivery AS
SELECT id,name,salary,area,busy
FROM delivery
''')

cur.execute('''CREATE VIEW Delcustomer AS
SELECT id,name,area,phoneNumber
FROM customer
''')
cur.execute('''CREATE VIEW Delorder AS
SELECT id,restaurantId
FROM orderr
''')
cur.execute('''CREATE VIEW Delsending AS
SELECT orderId,deliveryId,arrivingTime,cost
FROM sending
''')

con.commit()
print("views of delivery created successfully")
con.close()