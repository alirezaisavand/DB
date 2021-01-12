import psycopg2

con = psycopg2.connect(database="testdb", user="postgres", password="...", host="127.0.0.1", port="5433")

cur = con.cursor()

cur.execute('''drop table foodOrdered''')
cur.execute('''drop table sending''')
cur.execute('''drop table orderr''')
cur.execute('''drop table food''')
cur.execute('''drop table restaurant''')
cur.execute('''drop table delivery''')
cur.execute('''drop table discountCode''')
cur.execute('''drop table basket''')
cur.execute('''drop table customer''')

print("Done!")

con.commit()
con.close()
