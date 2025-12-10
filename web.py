import time
import pymysql
from flask import Flask, request, jsonify

# Mechanizm retry – czekaj na start MySQL
for i in range(12):  # 12 prób po 5 sekund = 1 minuta
    try:
        connection = pymysql.connect(
            host='mysql-db',
            user='user',
            password='pass',
            db='appdb'
        )
        print("Connected to MySQL!")
        break
    except pymysql.err.OperationalError:
        print("MySQL not ready, sleeping...")
        time.sleep(5)
else:
    print("Could not connect to MySQL after retries.")
    exit(1)

app = Flask(__name__)

def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(255) NOT NULL
        );
        """)
    connection.commit()

create_table()

@app.route('/items', methods=['GET'])
def get_items():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM items")
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO items (name) VALUES (%s)", (data['name'],))
        connection.commit()
    return jsonify({"message": "Item added"}), 201

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

