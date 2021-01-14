import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"], password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])
token_length = data["postgresql"]["token_length"]
name_length = data["postgresql"]["name_length"]
phone_length = data["postgresql"]["phone_length"]
description_length = data["postgresql"]["description_length"]

cur = con.cursor()
cur.execute('''create trigger score_handler on foodOrdered after update,insert,delete ''')

con.commit()
con.close()
