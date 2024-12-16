from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

DATABASE_CONFIG = "Driver={SQL Server};Server=localhost;Database=InventoryServiceDB;Trusted_Connection=yes;"

@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    room_number = data['room_number']
    room_type = data['room_type']
    status = data['status']

    conn = pyodbc.connect(DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (room_number, room_type, status)
        VALUES (?, ?, ?)
    """, (room_number, room_type, status))
    conn.commit()
    conn.close()
    return jsonify({"message": "Room created"}), 201

@app.route('/rooms/<int:room_id>', methods=['PATCH'])
def update_room_status(room_id):
    data = request.json
    status = data['status']

    conn = pyodbc.connect(DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("UPDATE rooms SET status = ? WHERE room_id = ?", (status, room_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Room status updated"}), 200

if __name__ == '__main__':
    app.run(debug=True)
