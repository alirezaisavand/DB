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
        phoneNumber character('''+phone_length+'''),
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
        restaurantid character('''+token_length+'''),
        score real,
        foreign key (restaurantid) references restaurant(id));''')

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
        phoneNumber character('''+phone_length+'''),
        balance integer);''')


cur.execute('''create table discountCode
        (id character('''+token_length+''') primary key not null,
        percentage integer,
        max integer,
        custId character('''+token_length+'''),
        foreign key (custId) references customer(id));''')

cur.execute('''create table basket
        (customerId character('''+token_length+''') not null,
        foodId character('''+token_length+''') not null,
        amount integer,
        primary key(customerId, foodId));''')

cur.execute('''create table orderr
        (id character('''+token_length+''') primary key not null,
        restaurantId character('''+token_length+''') not null,
        customerId character('''+token_length+''') not null,
        discountId character('''+token_length+''') not null,
        preparingTime timestamp,
        orderTime timestamp,
        foreign key (restaurantId) references restaurant(id),
        foreign key (customerId) references customer(id),
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

cur.execute('''create table foodOrdered
        (orderId character('''+token_length+''') not null,
        foodId character('''+token_length+'''),
        score integer,
        primary key (orderId, foodId),
        foreign key (orderId) references orderr(id),
        foreign key (foodId) references food(id));''')



print("create tables are Done!")

con.commit()
con.close()
