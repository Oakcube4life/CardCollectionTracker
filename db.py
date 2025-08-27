#This is for all DB actions like adding cards or searching cards that you have MAYBE REMOVE THIS ALL IDK at 
#least move the majoritly of it to the backend.py or vice versa?

import sqlite3
from datetime import datetime

DB_FILE = "pokemon_cards.db"

def get_card_from_db(card_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT name, set_name, card_number FROM cards WHERE id = ?", (card_id,))
    row = cur.fetchone()

    conn.close()

    return row

def get_cards_from_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    conn.row_factory = sqlite3.Row  # lets us return dict-like rows
    cur = conn.cursor()

    cur.execute("SELECT * FROM cards")

    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def add_card_to_db(img, name, set_name, card_number, price):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cards (img, name, set_name, card_number, date_added, price_when_added, current_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (img, name, set_name, card_number, datetime.now().strftime("%Y-%m-%d"), price, price))
    conn.commit()
    conn.close()
    return cur.lastrowid

def refresh_card_in_db(card_id, new_price):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("UPDATE cards SET current_price = ? WHERE id = ?", (new_price, card_id))

    conn.commit()
    conn.close()


def remove_card_from_db(card_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()
    