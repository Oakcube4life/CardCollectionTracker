# Run this once to startup your db.

import sqlite3

# Connect to your database
conn = sqlite3.connect("pokemon_cards.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    img TEXT NOT NULL,
    name TEXT NOT NULL,
    set_name TEXT NOT NULL,
    card_number TEXT NOT NULL,
    date_added TEXT NOT NULL,
    price_when_added REAL NOT NULL,
    current_price REAL NOT NULL
)""")

conn.close()