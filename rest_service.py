from flask import Flask, request, jsonify
import requests
import pyodbc

app = Flask(__name__)

DATABASE_CONFIG = "Driver={SQL Server};Server=localhost;Database=RESTServiceDB;Trusted_Connection=yes;"

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    room_type = data['room_type']
    start_date = data['start_date']
    end_date = data['end_date']
    customer_name = data['customer_name']

    # Verificar disponibilidad llamando al servicio SOAP
    soap_response = requests.post(
        "http://127.0.0.1:8000/",
        data=f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:lux="luxurystay.soap">
           <soapenv:Header/>
           <soapenv:Body>
              <lux:check_availability>
                 <start_date>{start_date}</start_date>
                 <end_date>{end_date}</end_date>
                 <room_type>{room_type}</room_type>
              </lux:check_availability>
           </soapenv:Body>
        </soapenv:Envelope>
        """,
        headers={"Content-Type": "text/xml"}
    )

    if "<Room>" not in soap_response.text:
        return jsonify({"error": "No rooms available"}), 400

    # Registrar la reserva
    conn = pyodbc.connect(DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reservations (room_number, customer_name, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (101, customer_name, start_date, end_date, 'Activa'))
    conn.commit()
    conn.close()
    return jsonify({"message": "Reservation created"}), 201

# Consultar reserva
@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    conn = pyodbc.connect(DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservations WHERE reservation_id = ?", reservation_id)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Reservation not found"}), 404

    return jsonify({
        "reservation_id": row.reservation_id,
        "room_number": row.room_number,
        "customer_name": row.customer_name,
        "start_date": row.start_date,
        "end_date": row.end_date,
        "status": row.status
    })

# Cancelar reserva
@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    conn = pyodbc.connect(DATABASE_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE reservation_id = ?", reservation_id)
    conn.commit()
    conn.close()
    return jsonify({"message": "Reservation cancelled"}), 200

if __name__ == '__main__':
    app.run(debug=True)
