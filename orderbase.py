from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Database setup
DATABASE = 'order_data.db'

def init_order_db():
    """Initialize the database if it does not exist."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Create users table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id TEXT PRIMARY KEY,  -- Firebase UID
                                name TEXT NOT NULL UNIQUE
                              )''')
            
            # Create orders table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    items TEXT NOT NULL, -- JSON string including quantity
                    total_price REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    order_date TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

@app.route('/add_order', methods=['POST'])
def add_order():
    """Endpoint to add an order to the database."""
    data = request.get_json()
    user_id = data.get('user_id')  # Firebase UID from the frontend
    items = data.get('items')  # List of items in the order
    total_price = data.get('total_price')  # Total price of the order
    payment_method = data.get('payment_method')  # Payment method (e.g., 'Credit Card')
    
    if not user_id or not items or total_price is None or not payment_method:
        return jsonify({"message": "User ID, Items, Total Price, and Payment Method are required"}), 400

    try:
        # Convert items list to JSON string for storage
        items_json = json.dumps(items)
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO orders (user_id, items, total_price, payment_method, order_date) 
                              VALUES (?, ?, ?, ?, ?)''', 
                           (user_id, items_json, total_price, payment_method, order_date))
            conn.commit()

        return jsonify({"message": "Order placed successfully!"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

@app.route('/get_orders', methods=['GET'])
def get_orders():
    """Endpoint to retrieve all orders from the database."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT order_id, user_id, items, total_price, payment_method, order_date FROM orders")
            orders = cursor.fetchall()

        # Convert orders data into a list of dictionaries
        orders_list = [{
            "order_id": order[0],
            "user_id": order[1],
            "items": json.loads(order[2]),  # Convert items JSON string back to list
            "total_price": order[3],
            "payment_method": order[4],
            "order_date": order[5]
        } for order in orders]

        return jsonify({"orders": orders_list}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

@app.route('/get_order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Endpoint to retrieve a specific order by its ID."""
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT order_id, user_id, items, total_price, payment_method, order_date FROM orders WHERE order_id = ?", (order_id,))
            order = cursor.fetchone()

        if order:
            order_data = {
                "order_id": order[0],
                "user_id": order[1],
                "items": json.loads(order[2]),  # Convert items JSON string back to list
                "total_price": order[3],
                "payment_method": order[4],
                "order_date": order[5]
            }
            return jsonify({"order": order_data}), 200
        else:
            return jsonify({"message": "Order not found"}), 404

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

if __name__ == '__main__':
    init_order_db()  # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=5000, debug=True)
