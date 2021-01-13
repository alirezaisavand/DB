import psycopg2
import json

f = open('config_file.JSON')
data = json.load(f)
con = psycopg2.connect(database=data["postgresql"]["database"], user=data["postgresql"]["user"], password=data["postgresql"]["password"], host=data["postgresql"]["host"], port=data["postgresql"]["port"])

cur = con.cursor()

cur.execute('''create table restaurant
        (id character(30) primary key not null,
        name character(30),
        phoneNumber character(30),
        area character(30),
        type character(30),
        score real,
        minOrder integer);''')

cur.execute('''create table food
        (id character(30) primary key not null,
        name character(30),
        type character(30),
        amount integer,
        description character(30),
        price integer,
        restaurantid character(30),
        score real,
        foreign key (restaurantid) references restaurant(id));''')

cur.execute('''create table delivery
        (id character(30) primary key not null,
        name character(30),
        salary integer,
        area character(30),
        busy boolean);''')

cur.execute('''create table customer
        (id character(30) primary key not null,
        name character(30),
        area character(30),
        phoneNumber character(30),
        balance integer);''')


cur.execute('''create table discountCode
        (id character(30) primary key not null,
        percentage integer,
        max integer,
        custId character(30),
        foreign key (custId) references customer(id));''')

cur.execute('''create table basket
        (customerId character(30) not null,
        foodId character(30) not null,
        amount integer,
        primary key(customerId, foodId));''')

cur.execute('''create table orderr
        (id character(30) primary key not null,
        restaurantId character(30) not null,
        customerId character(30) not null,
        discountId character(30) not null,
        preparingTime integer,
        orderTime integer,
        foreign key (restaurantId) references restaurant(id),
        foreign key (customerId) references customer(id),
        foreign key (discountId) references discountCode(id));''')

cur.execute('''create table sending
        (orderId character(30) not null,
        deliveryId character(30) not null,
        score integer,
        arrivingTime integer,
        cost integer,
        primary key (orderId, deliveryId),
        foreign key (orderId) references orderr(id),
        foreign key (deliveryId) references delivery(id));''')

cur.execute('''create table foodOrdered
        (orderId character(30) not null,
        foodId character(30),
        score integer,
        primary key (orderId, foodId),
        foreign key (orderId) references orderr(id),
        foreign key (foodId) references food(id));''')


print("create tables are Done!")

con.commit()
con.close()
