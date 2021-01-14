import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])

cur = con.cursor()




cur.execute('''CREATE VIEW Cusrestaurant AS
SELECT id,name,phone_number,area,type,min_order,score
FROM restaurant
''')
cur.execute('''CREATE VIEW Cusdelivery AS
SELECT id,name
FROM delivery
''')
cur.execute('''CREATE VIEW CusdiscountCode AS
SELECT id,percentage,max,customer_id
FROM discountCode
''')
cur.execute('''CREATE VIEW Cuscustomer AS
SELECT id,name,area,phone_number,balance
FROM customer
''')
cur.execute('''CREATE VIEW Cusbasket AS
SELECT customer_id,food_id,amount
FROM basket
''')
cur.execute('''CREATE VIEW Cusorder AS
SELECT id,restaurant_id,preparing_time,customer_id,order_time,discount_id, total_price
FROM orderr
''')
cur.execute('''CREATE VIEW Cussending AS
SELECT order_id,delivery_id,score,arriving_time,cost
FROM sending
''')
cur.execute('''CREATE VIEW CusfoodOrdered AS
SELECT order_id,food_id,score
FROM food_ordered
''')

cur.execute('''CREATE VIEW Cusfood AS
SELECT id,name,type,amount,description,price,restaurant_id,score
FROM food
''')

con.commit()
print("views of Customer created successfully")

cur.execute('''CREATE VIEW Delrestaurant AS
SELECT id,name,phone_number,area
FROM restaurant
''')
cur.execute('''CREATE VIEW Deldelivery AS
SELECT id,name,salary,area,busy
FROM delivery
''')

cur.execute('''CREATE VIEW Delcustomer AS
SELECT id,name,area,phone_number
FROM customer
''')
cur.execute('''CREATE VIEW Delorder AS
SELECT id,restaurant_id
FROM orderr
''')
cur.execute('''CREATE VIEW Delsending AS
SELECT order_id,delivery_id,arriving_time,cost
FROM sending
''')
print("views of delivery created successfully")

cur.execute('''CREATE VIEW Resrestaurant AS SELECT id, name, phone_number, area, type, min_order from restaurant''')
cur.execute('''CREATE VIEW Resfood AS SELECT id, name, type, amount, description, price, restaurant_id from food''')
cur.execute('''CREATE VIEW Resdelivery AS SELECT id,name,area,busy FROM delivery''')
cur.execute('''CREATE VIEW Rescustomer AS SELECT id,name,area,phone_number from customer''')
cur.execute('''CREATE VIEW Resorder AS SELECT id,restaurant_id,preparing_time,customer_id,order_time, total_price from orderr''')
cur.execute('''CREATE VIEW Ressending AS SELECT order_id,delivery_id from sending''')
cur.execute('''CREATE VIEW ResfoodOrdered AS SELECT order_id,food_id from food_ordered''')


print("views of restaurant created successfully")
con.commit()