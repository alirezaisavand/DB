import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"],password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])

cur = con.cursor()

cur.execute('''drop table user_pass''')
cur.execute('''drop table food_ordered''')
cur.execute('''drop table sending''')
cur.execute('''drop table orderr''')
cur.execute('''drop table basket''')
cur.execute('''drop table discountCode''')
cur.execute('''drop table customer''')
cur.execute('''drop table delivery''')
cur.execute('''drop table food''')
cur.execute('''drop table restaurant''')

print("Drop all tables Done!")

con.commit()
