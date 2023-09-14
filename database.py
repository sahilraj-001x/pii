import sqlite3

conn = sqlite3.connect('pii.db')

c = conn.cursor()

c.execute("""CREATE TABLE pii_table(
        id primar
        )""")