from flask import Flask, request, render_template, jsonify
from db import add_card_to_db, get_card_from_db, get_cards_from_db, remove_card_from_db, refresh_card_in_db
from scraper import get_card_price, get_img_link
from datetime import datetime

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

# Endpoint to get all cards (When site loads)
@app.route("/get_cards", methods=["GET"])
def get_cards():
    return get_cards_from_db()

# Endpoint to add a card
@app.route("/add_card", methods=["POST"])
def add_card():
    try:
        data = request.get_json(force=True)

        name = data["name"]
        set_name = data["set_name"]
        card_number = data["card_number"]

        # Get Card Img Link
        img = get_img_link(name, set_name, card_number)

        # Scrape the card price
        price = get_card_price(name, set_name, card_number)

        # Insert into SQLite and return the id
        card_id = add_card_to_db(img, name, set_name, card_number, price)

        # Both prices are identical here on purpose
        return jsonify({"status": "success", "id": card_id, "img": img, "date_added": datetime.now().strftime("%Y-%m-%d"), "price": price})

    except Exception as e:
        print("Error in /add_card:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/refresh_card/<int:card_id>", methods=["POST"])
def refresh_card(card_id):
    card_data = get_card_from_db(card_id)
    new_price = get_card_price(card_data[0], card_data[1], card_data[2])

    refresh_card_in_db(card_id, new_price)

    return jsonify({"price": new_price})

@app.route("/remove_card/<int:card_id>", methods=["DELETE"])
def remove_card(card_id):
    price = remove_card_from_db(card_id)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
