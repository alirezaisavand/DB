import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"], password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])

cur = con.cursor()

cur.execute('''drop view Cusfood''')
cur.execute('''drop view Cusrestaurant''')
cur.execute('''drop view Cusdelivery''')
cur.execute('''drop view CusdiscountCode''')
cur.execute('''drop view Cuscustomer''')
cur.execute('''drop view Cusbasket''')
cur.execute('''drop view Cusorder''')
cur.execute('''drop view Cussending''')
cur.execute('''drop view CusfoodOrdered''')

print("Drop all Customer views Done!")

con.commit()

cur.execute('''drop view Delrestaurant''')
cur.execute('''drop view Deldelivery''')
cur.execute('''drop view Delcustomer''')
cur.execute('''drop view Delorder''')
cur.execute('''drop view Delsending''')

con.commit()
print("Drop all delivery views Done!")

cur.execute('''drop view Resrestaurant''')
cur.execute('''drop view Resfood''')
cur.execute('''drop view Resdelivery''')
cur.execute('''drop view Rescustomer''')
cur.execute('''drop view Resorder''')
cur.execute('''drop view Ressending''')
cur.execute('''drop view ResfoodOrdered''')

con.commit()
print("Drop all restaurant views Done!")
