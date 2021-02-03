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
        phone_number character('''+phone_length+''') 
        CONSTRAINT proper_phone CHECK (phone_number ~* '^[0-9]'),
        area character('''+name_length+'''),
        type character('''+name_length+'''),
        score real DEFAULT 2.5 CHECK(score>=0 and score<=5),
        min_order integer CHECK(min_order>=0) ); ''')

cur.execute('''create table food
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+'''),
        type character('''+name_length+'''),
        amount integer CHECK(amount >=0),
        description character('''+description_length+'''),
        price integer CHECK(price >=0),
        restaurant_id character('''+token_length+'''),
        score real DEFAULT 2.5 CHECK(score>=0 and score<=5),
        foreign key (restaurant_id) references restaurant(id));''')

cur.execute('''create table delivery
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+''')
        CONSTRAINT proper_name CHECK (name ~* '^[a-zA-Z]'),
        salary integer CHECK(salary >0),
        area character('''+name_length+'''),
        busy boolean);''')

cur.execute('''create table customer
        (id character('''+token_length+''') primary key not null,
        name character('''+name_length+''') 
        CONSTRAINT proper_name CHECK (name ~* '^[a-zA-Z]'),
        area character('''+name_length+'''),
        phone_number character('''+phone_length+''') 
        CONSTRAINT proper_phone CHECK (phone_number ~* '^[0-9]'),
        balance integer CHECK(balance >=0));''')


cur.execute('''create table discountCode
        (id character('''+token_length+''') primary key not null,
        percentage real CHECK(percentage >0 and percentage<=1),
        max integer CHECK(max >0),
        customer_id character('''+token_length+'''),
        used boolean,
        foreign key (customer_id) references customer(id));''')

cur.execute('''create table basket
        (customer_id character('''+token_length+''') not null,
        food_id character('''+token_length+''') not null,
        amount integer CHECK(amount >=0),
        primary key(customer_id, food_id));''')

cur.execute('''create table orderr
        (id character('''+token_length+''') primary key not null,
        restaurant_id character('''+token_length+''') not null,
        customer_id character('''+token_length+''') not null,
        discount_id character('''+token_length+''') ,
        preparing_time timestamp,
        order_time timestamp,
        total_price integer CHECK(total_price >=0),
        foreign key (restaurant_id) references restaurant(id),
        foreign key (customer_id) references customer(id),
        foreign key (discount_id) references discountCode(id));''')

cur.execute('''create table sending
        (order_id character('''+token_length+''') not null,
        delivery_id character('''+token_length+''') not null,
        score integer DEFAULT 2.5 CHECK(score>=0 and score<=5),
        arriving_time timestamp,
        cost integer CHECK(cost >=0),
        primary key (order_id, delivery_id),
        foreign key (order_id) references orderr(id),
        foreign key (delivery_id) references delivery(id));''')

cur.execute('''create table food_ordered
        (order_id character('''+token_length+''') not null,
        food_id character('''+token_length+'''),
        amount integer CHECK(amount >=0),
        score integer DEFAULT 2.5 CHECK(score>=0 and score<=5),
        primary key (order_id, food_id),
        foreign key (order_id) references orderr(id),
        foreign key (food_id) references food(id));''')

cur.execute('''create table user_pass
        (customer_id character('''+token_length+''') not null,
        password character('''+token_length+''') not null
        CONSTRAINT password_with_number CHECK (password ~* '.*[0-9].*')
        CONSTRAINT password_with_char CHECK (password ~* '.*[a-zA-Z].*'),
        primary key (customer_id)
        );''')

cur.execute('''create table res_user_pass(
            restaurant_id character('''+token_length+''') not null,
            password character('''+token_length+''') not null,
            CONSTRAINT password_with_number CHECK (password ~* '.*[0-9].*')
            CONSTRAINT password_with_char CHECK (password ~* '.*[a-zA-Z].*'),
     
            primary key (restaurant_id)
            );''')

cur.execute('''create table del_user_pass(
            delivery_id character('''+token_length+''') not null,
            username character('''+token_length+''') not null,
            password character('''+token_length+''') not null,
            primary key (delivery_id)
            );''')

print("create tables are Done!")

con.commit()
