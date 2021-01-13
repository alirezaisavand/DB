import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])

cur = con.cursor()

cur.execute('''drop view CusfoodOrdered''')
cur.execute('''drop view Cusfood''')
cur.execute('''drop view Cussending''')
cur.execute('''drop view Cusorder''')
cur.execute('''drop view Cusrestaurant''')
cur.execute('''drop view Cusdelivery''')
cur.execute('''drop view CusdiscountCode''')
cur.execute('''drop view Cusbasket''')
cur.execute('''drop view Cuscustomer''')

print("Drop all Customer views Done!")

con.commit()

cur.execute('''drop view Delsending''')
cur.execute('''drop view Delorder''')
cur.execute('''drop view Delrestaurant''')
cur.execute('''drop view Deldelivery''')
cur.execute('''drop view Delcustomer''')

print("Drop all delivery views Done!")

con.commit()

con.close()
