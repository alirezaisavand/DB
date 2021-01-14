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
cur.execute('''create table restaurant
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+'''),
        phone_number character('''+phone_length+'''),
        area character('''+name_length+'''),
        type character('''+name_length+'''),
        score real,
        minOrder integer);''')

cur.execute('''create table food
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+'''),
        type character('''+name_length+'''),
        amount integer,
        description character('''+description_length+'''),
        price integer,
        restaurant_id character('''+token_length+'''),
        score real,
        foreign key (restaurant_id) references restaurant(id));''')

cur.execute('''create table delivery
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+'''),
        salary integer,
        area character('''+name_length+'''),
        busy boolean);''')

cur.execute('''create table customer
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+'''),
        area character('''+name_length+'''),
        phone_number character('''+phone_length+'''),
        balance integer);''')


cur.execute('''create table discountCode
        (id character('''+token_length+''') primary key not null,
        percentage integer,
        max integer,
        custId character('''+token_length+'''),
        foreign key (custId) references customer(id));''')

cur.execute('''create table basket
        (customer_id character('''+token_length+''') not null,
        food_id character('''+token_length+''') not null,
        amount integer,
        primary key(customer_id, food_id));''')

cur.execute('''create table orderr
        (id character('''+token_length+''') primary key not null,
        restaurant_id character('''+token_length+''') not null,
        customer_id character('''+token_length+''') not null,
        discountId character('''+token_length+''') not null,
        preparingTime timestamp,
        orderTime timestamp,
        total_price integer,
        foreign key (restaurant_id) references restaurant(id),
        foreign key (customer_id) references customer(id),
        foreign key (discountId) references discountCode(id));''')

cur.execute('''create table sending
        (orderId character('''+token_length+''') not null,
        deliveryId character('''+token_length+''') not null,
        score integer,
        arrivingTime timestamp,
        cost integer,
        primary key (orderId, deliveryId),
        foreign key (orderId) references orderr(id),
        foreign key (deliveryId) references delivery(id));''')

cur.execute('''create table food_ordered
        (orderId character('''+token_length+''') not null,
        food_id character('''+token_length+'''),
        score integer,
        primary key (orderId, food_id),
        foreign key (orderId) references orderr(id),
        foreign key (food_id) references food(id));''')

cur.execute('''create table user_pass
        (customer_id character('''+token_length+''') not null,
        password character('''+token_length+''') not null);''')


print("create tables are Done!")

con.commit()
con.close()
