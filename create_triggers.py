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

cur.execute('''CREATE OR REPLACE FUNCTION food_score()
  RETURNS trigger AS
$$
BEGIN
    update food set score = (
            select avg(score) from food_ordered 
            where food_ordered.food_id = food.id 
            ) where food.id = new.food_id;     
 
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';''')

cur.execute('''create trigger food_score_handler
            after update of score on food_ordered
            for each row
            when (new.score is not null)
            execute procedure food_score();''')

cur.execute('''CREATE OR REPLACE FUNCTION restaurant_score()
  RETURNS trigger AS
$$
BEGIN
    update restaurant set score = (
                select avg(score) from food where food.restaurant_id = restaurant.id
            ) where restaurant.id = new.restaurant_id;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';''')

cur.execute('''create trigger restaurant_score_handler
            after update of score on food
            for each row
            execute procedure restaurant_score()''')

cur.execute('''CREATE OR REPLACE FUNCTION delivery_busy()
  RETURNS trigger AS
$$
BEGIN
    update delivery set busy = true where id = new.delivery_id;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';''')

cur.execute('''create trigger set_delivery_busy
            after insert on ressending
            execute procedure delivery_busy()''')

cur.execute('''CREATE OR REPLACE FUNCTION delivery_free()
  RETURNS trigger AS
$$
BEGIN
    update delivery set busy = false where id = new.delivery_id;
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';''')

cur.execute('''create trigger set_delivery_free
            after insert on ressending
            execute procedure delivery_free()''')

con.commit()
