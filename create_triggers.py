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
#check kon ino
cur.execute('''create trigger food_score_handler 
            after update of score on food_ordered
            referencing new as n1 old as o1 
            for each row
            when (n1.score is not null)
            begin
            update food set score = (
            select avg(score) from food_ordered 
            where foodOrdered.food_id = food.id 
            ) where food.id = n1.food_id
            end''')

cur.execute('''create trigger restaurant_score_handler
            after update of score on food
            referencing new as n1 old as o1
            for each row
            begin
            update restaurant set score = (
                select avg(score) from food where food.restaurant_id = restaurant.id
            ) where restaurant.id = n1.restaurant_id 
            end''')

con.commit()
